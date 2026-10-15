"""Config flow for Tuya Heat Pump integration."""
from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_ACCESS_ID,
    CONF_ACCESS_KEY,
    CONF_DEVICE_ID,
    CONF_REGION,
    CONF_SCAN_INTERVAL,
    CONF_CONNECTION_TYPE,
    CONF_IP,
    CONF_LOCAL_KEY,
    CONF_PROTOCOL,
    DEFAULT_SCAN_INTERVAL,
    REGIONS,
    DEFAULT_REGION,
    PROTOCOL_OPTIONS,
    CONF_USER_CODE,
    CONF_SHARING_TOKEN_INFO,
    CONF_CLIMATE_ENABLED,
    CONF_CLIMATE_POWER_CODE,
    CONF_CLIMATE_CURRENT_TEMP_CODE,
    CONF_CLIMATE_TARGET_TEMP_CODE,
    CONF_CLIMATE_MODE_SELECT_CODE,
    CONF_CLIMATE_HEAT_VALUE,
    CONF_CLIMATE_COOL_VALUE,
    CONF_CLIMATE_TOLERANCE,
    CONF_CLIMATE_MIN_CYCLE_MINUTES,
    CONF_CLIMATE_MIN_TEMP,
    CONF_CLIMATE_MAX_TEMP,
    DEFAULT_CLIMATE_TOLERANCE,
    DEFAULT_CLIMATE_MIN_CYCLE_MINUTES,
    DEFAULT_CLIMATE_MIN_TEMP,
    DEFAULT_CLIMATE_MAX_TEMP,
)
from .coordinator import TuyaScaleDataUpdateCoordinator
from .sharing_mqtt import SharingQRLogin
import tinytuya

_LOGGER = logging.getLogger(__name__)


# --- Opsiyonel climate (termostat) entity'si için yardımcılar ---
# Hem ilk kurulumun (TuyaHeatpumpConfigFlow) hem de Options akışının
# (TuyaHeatpumpOptionsFlow) sonunda aynı formları gösteriyoruz; bu
# fonksiyonlar ikisi arasında paylaşılıyor.

def _is_temperature_field(cfg: dict) -> bool:
    """A plain NUMBER/SENSOR dict entry that represents a temperature,
    regardless of whether the model file tagged it with device_class or
    just a °C/°F unit."""
    return cfg.get("device_class") == "temperature" or cfg.get("unit") in ("°C", "°F")


def _climate_option_list(mapping: dict, *, temperature_only: bool) -> list:
    """Dropdown options built straight from a model's own dict keys.
    Raw-field DPs (field_index) are skipped — the climate bridge only
    supports plain DPs, same as every other code path here that reads
    coordinator.data directly."""
    options = []
    for key, cfg in mapping.items():
        if "field_index" in cfg:
            continue
        if temperature_only and not _is_temperature_field(cfg):
            continue
        label = cfg.get("name", key)
        options.append(selector.SelectOptionDict(value=key, label=f"{label} ({key})"))
    return options


def _select_raw_keys(cfg: dict) -> list:
    """A SELECT_TYPES entry's real Tuya enum values (the dict keys when
    'options' is a {raw: label} map, or the list itself otherwise) —
    what actually gets read from/written to the device, as opposed to
    the human-readable label select.py shows in the UI."""
    options_dict = cfg.get("options", {})
    if isinstance(options_dict, dict):
        return list(options_dict.keys())
    return list(options_dict)


def _select_option_list(selects: dict) -> list:
    """Dropdown options for picking WHICH select entity is the heat/cool
    mode select (plain DPs only, same rule as _climate_option_list)."""
    options = []
    for key, cfg in selects.items():
        if "field_index" in cfg:
            continue
        label = cfg.get("name", key)
        options.append(selector.SelectOptionDict(value=key, label=f"{label} ({key})"))
    return options


def _select_value_option_list(select_cfg: dict) -> list:
    """Dropdown options for picking a specific raw value out of one
    (already chosen) select entity's own option list."""
    options_dict = select_cfg.get("options", {})
    options = []
    for key in _select_raw_keys(select_cfg):
        label = options_dict.get(key, key) if isinstance(options_dict, dict) else key
        options.append(selector.SelectOptionDict(value=key, label=f"{label} ({key})"))
    return options


def _guess_heat_cool_values(select_cfg: dict) -> dict:
    """Best-effort guess at which of a select's own raw values means
    heat/cool, by substring match — same generic, no-model-hardcoded
    approach as the rest of this file. Always editable afterwards."""
    raw_keys = _select_raw_keys(select_cfg)
    guesses: dict = {}

    heat = next((k for k in raw_keys if "heat" in k.lower() and "cool" not in k.lower()), None) \
        or next((k for k in raw_keys if "heat" in k.lower()), None)
    cool = next((k for k in raw_keys if "cool" in k.lower() and "heat" not in k.lower()), None) \
        or next((k for k in raw_keys if "cool" in k.lower()), None)

    if heat:
        guesses["heat_value"] = heat
    if cool:
        guesses["cool_value"] = cool
    return guesses


def _detect_climate_defaults(model_mapping: dict) -> dict:
    """Best-effort suggestions only — every field below stays editable
    and can be left blank. No model file is special-cased here; this is
    a single generic rule applied uniformly to all of them:

    - Power: every known model exposes a switch literally called/coded
      "Power", so that one is always safe to default to.
    - Target: only on models whose OWN firmware already runs closed-loop
      ROOM-temperature control (as opposed to a water/tank setpoint) is
      there a settable "room"/"indoor" temperature number — on those we
      default target+current to that pair. On a plain water-only model
      (the majority here), nothing matches and both stay blank.
    - Mode select: a select DP whose own raw values include both a
      heat-like and a cool-like one (the repo's own "work_mode"
      convention) — when found, also guesses which raw value is which."""
    switches = model_mapping.get("switches", {})
    numbers = model_mapping.get("numbers", {})
    sensors = model_mapping.get("sensors", {})
    selects = model_mapping.get("selects", {})

    defaults: dict = {}

    for key, cfg in switches.items():
        if "field_index" in cfg:
            continue
        if key.lower() == "power" or str(cfg.get("code", "")).lower() == "power":
            defaults["power"] = key
            break

    target_key = None
    for key, cfg in numbers.items():
        if "field_index" in cfg or not _is_temperature_field(cfg):
            continue
        haystack = f"{key} {cfg.get('name', '')}".lower()
        if ("room" in haystack or "indoor" in haystack) and ("set" in haystack or "target" in haystack):
            target_key = key
            break

    if target_key:
        defaults["target"] = target_key
        for key, cfg in sensors.items():
            if "field_index" in cfg or not _is_temperature_field(cfg):
                continue
            haystack = f"{key} {cfg.get('name', '')}".lower()
            if "room" in haystack or "indoor" in haystack:
                defaults["current"] = key
                break

    mode_select_key = None
    work_mode_cfg = selects.get("work_mode")
    if work_mode_cfg is not None and "field_index" not in work_mode_cfg:
        guess = _guess_heat_cool_values(work_mode_cfg)
        if "heat_value" in guess and "cool_value" in guess:
            mode_select_key = "work_mode"
    if mode_select_key is None:
        for key, cfg in selects.items():
            if "field_index" in cfg:
                continue
            guess = _guess_heat_cool_values(cfg)
            if "heat_value" in guess and "cool_value" in guess:
                mode_select_key = key
                break

    if mode_select_key:
        defaults["mode_select"] = mode_select_key
        defaults.update(_guess_heat_cool_values(selects[mode_select_key]))

    return defaults


def _climate_options_schema(model_mapping: dict | None, current: dict) -> vol.Schema:
    """Build the climate_options form schema from a model's own DPs,
    pre-filled with the auto-detected defaults (or, on an already
    configured entry, whatever the user picked last time)."""
    model_mapping = model_mapping or {}
    defaults = _detect_climate_defaults(model_mapping)

    power_options = _climate_option_list(model_mapping.get("switches", {}), temperature_only=False)
    current_temp_options = _climate_option_list(
        {**model_mapping.get("sensors", {}), **model_mapping.get("numbers", {})},
        temperature_only=True,
    )
    target_temp_options = _climate_option_list(model_mapping.get("numbers", {}), temperature_only=True)
    mode_select_options = _select_option_list(model_mapping.get("selects", {}))

    none_option = [selector.SelectOptionDict(value="", label="— none / leave blank —")]

    return vol.Schema(
        {
            vol.Optional(
                CONF_CLIMATE_ENABLED,
                default=current.get(CONF_CLIMATE_ENABLED, False),
            ): selector.BooleanSelector(),
            vol.Optional(
                CONF_CLIMATE_POWER_CODE,
                default=current.get(CONF_CLIMATE_POWER_CODE) or defaults.get("power", ""),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=none_option + power_options,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Optional(
                CONF_CLIMATE_CURRENT_TEMP_CODE,
                default=current.get(CONF_CLIMATE_CURRENT_TEMP_CODE) or defaults.get("current", ""),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=none_option + current_temp_options,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Optional(
                CONF_CLIMATE_TARGET_TEMP_CODE,
                default=current.get(CONF_CLIMATE_TARGET_TEMP_CODE) or defaults.get("target", ""),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=none_option + target_temp_options,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Optional(
                CONF_CLIMATE_MODE_SELECT_CODE,
                default=current.get(CONF_CLIMATE_MODE_SELECT_CODE) or defaults.get("mode_select", ""),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=none_option + mode_select_options,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Optional(
                CONF_CLIMATE_TOLERANCE,
                default=current.get(CONF_CLIMATE_TOLERANCE, DEFAULT_CLIMATE_TOLERANCE),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0.1, max=5, step=0.1, mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="°C",
                )
            ),
            vol.Optional(
                CONF_CLIMATE_MIN_CYCLE_MINUTES,
                default=current.get(CONF_CLIMATE_MIN_CYCLE_MINUTES, DEFAULT_CLIMATE_MIN_CYCLE_MINUTES),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0, max=60, step=1, mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="min",
                )
            ),
            vol.Optional(
                CONF_CLIMATE_MIN_TEMP,
                default=current.get(CONF_CLIMATE_MIN_TEMP, DEFAULT_CLIMATE_MIN_TEMP),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=-20, max=100, step=1, mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="°C",
                )
            ),
            vol.Optional(
                CONF_CLIMATE_MAX_TEMP,
                default=current.get(CONF_CLIMATE_MAX_TEMP, DEFAULT_CLIMATE_MAX_TEMP),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=-20, max=100, step=1, mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="°C",
                )
            ),
        }
    )


def _climate_mode_values_schema(select_cfg: dict, current: dict) -> vol.Schema:
    """Second step, shown only if a mode select was picked above — lets
    the user confirm/correct which of ITS real option values means heat
    and which means cool."""
    value_options = _select_value_option_list(select_cfg)
    defaults = _guess_heat_cool_values(select_cfg)

    return vol.Schema(
        {
            vol.Optional(
                CONF_CLIMATE_HEAT_VALUE,
                default=current.get(CONF_CLIMATE_HEAT_VALUE) or defaults.get("heat_value", ""),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=value_options,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Optional(
                CONF_CLIMATE_COOL_VALUE,
                default=current.get(CONF_CLIMATE_COOL_VALUE) or defaults.get("cool_value", ""),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=value_options,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
        }
    )


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ACCESS_ID): str,
        vol.Required(CONF_ACCESS_KEY): str,
        vol.Required(CONF_DEVICE_ID): str,
        vol.Required(CONF_REGION, default=DEFAULT_REGION): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=list(REGIONS.keys()),
                mode=selector.SelectSelectorMode.DROPDOWN
            )
        ),
        vol.Required(CONF_CONNECTION_TYPE, default="cloud"): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    selector.SelectOptionDict(value="cloud", label="Cloud (Recommended for most users)"),
                    selector.SelectOptionDict(value="local", label="Local (Faster, no API limits)")
                ],
                mode=selector.SelectSelectorMode.DROPDOWN
            )
        ),
        # Opsiyonel — sadece Cloud modda anlamlı. Doldurulursa, kurulumun
        # sonunda bir QR kod gösterilir; Smart Life/Tuya Smart uygulamasıyla
        # onaylanırsa MQTT (anlık güncelleme) devreye girer. Boş bırakılırsa
        # (varsayılan, mevcut tüm kullanıcılar dahil) hiçbir şey değişmez,
        # entegrasyon eskisi gibi sadece periyodik sorgulamayla çalışır.
        vol.Optional(CONF_USER_CODE): str,
    }
)

STEP_LOCAL_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP): str,
        vol.Required(CONF_LOCAL_KEY): str,
        vol.Required(CONF_PROTOCOL, default="3.4"): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=PROTOCOL_OPTIONS,
                mode=selector.SelectSelectorMode.DROPDOWN
            )
        ),
    }
)

STEP_CLOUD_OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Optional(
            CONF_SCAN_INTERVAL,
            default=DEFAULT_SCAN_INTERVAL
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=1,
                max=60,
                step=1,
                mode=selector.NumberSelectorMode.BOX
            )
        ),
    }
)

STEP_LOCAL_OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP): str,
        vol.Required(CONF_LOCAL_KEY): str,
        vol.Required(CONF_PROTOCOL, default="3.4"): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=PROTOCOL_OPTIONS,
                mode=selector.SelectSelectorMode.DROPDOWN
            )
        ),
    }
)

async def validate_input(hass: HomeAssistant, data: dict, connection_type: str) -> dict:
    """Validate the user input allows us to connect."""
    # Kurulum doğrulaması için vekil ConfigEntry. Gerçek entry henüz
    # OLUŞMADI (onu ancak doğrulama başarılı olursa async_create_entry
    # oluşturacak), bu yüzden HA'nın config entry registry'sinde karşılığı
    # yok. entry_id'yi açıkça None veriyoruz: coordinator kalıcı yazma
    # yaparken (token/model cache) bunu görüp yazmayı atlıyor
    # (bkz. TuyaScaleDataUpdateCoordinator._persist_entry_data).
    mock_config = type(
        "MockConfigEntry",
        (),
        {
            "entry_id": None,
            "data": data,
            "options": {
                CONF_SCAN_INTERVAL: data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
            },
        },
    )()

    coordinator = TuyaScaleDataUpdateCoordinator(hass, mock_config)

    if connection_type == "cloud":
        try:
            # Token ve device info almayı dene
            if not coordinator.access_token:
                await coordinator._get_token()
            await coordinator.get_device_info()
        except Exception as err:
            _LOGGER.error("Cloud validation error: %s", err)
            if "token" in str(err).lower() or "auth" in str(err).lower():
                raise InvalidAuth("Invalid credentials") from err
            raise CannotConnect("Cannot connect to Tuya cloud") from err

        title = f"Tuya Heat Pump ({data[CONF_DEVICE_ID]})"

    else:
        # Local validation
        try:
            device = tinytuya.Device(
                dev_id=data[CONF_DEVICE_ID],
                address=data[CONF_IP],
                local_key=data[CONF_LOCAL_KEY],
                version=float(data[CONF_PROTOCOL]),
            )
            status = await hass.async_add_executor_job(device.status)
            if not status or 'dps' not in status:
                raise CannotConnect("Failed to get device status")
        except Exception as err:
            _LOGGER.error("Local validation error: %s", err)
            raise CannotConnect(f"Cannot connect to local device: {err}") from err

        title = f"Tuya Heat Pump Local ({data[CONF_DEVICE_ID]})"

    # Model mapping — Tuya'nın DP şeması her zaman cloud API'den gelir,
    # bağlantı tipi local olsa bile (bkz. coordinator.get_device_model
    # docstring'i, access_id/key her iki bağlantı tipinde de toplanıyor).
    # Burada en baştan çekiyoruz ki climate-entity eşleme ekranı
    # kurulumun SONUNDA (henüz hiçbir entity/coordinator kalıcı olarak
    # oluşmamışken) gerçek switch/sensor/number/select listesinden
    # dropdown gösterebilsin. Başarısız olursa (örn. model API'sine
    # erişilemedi) sessizce "default" mapping'e düşer ve climate adımı
    # sadece boş dropdown'lar gösterir — kurulumun geri kalanını
    # etkilemez.
    try:
        await coordinator.get_device_model()
    except Exception as err:
        _LOGGER.warning("Model mapping kurulum sırasında alınamadı: %s", err)

    return {"title": title, "model_mapping": coordinator.model_mapping or {}}


class TuyaHeatpumpOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self._config_entry = config_entry
        self.connection_type = config_entry.data.get(CONF_CONNECTION_TYPE, "cloud")
        self._pending_options: dict = {}

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if self.connection_type == "cloud":
            return await self.async_step_cloud_options()
        else:
            return await self.async_step_local_options()

    async def async_step_cloud_options(self, user_input=None):
        """Manage cloud options."""
        if user_input is not None:
            self._pending_options = dict(user_input)
            return await self.async_step_climate_options()

        return self.async_show_form(
            step_id="cloud_options",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self._config_entry.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        )
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=1,
                            max=60,
                            step=1,
                            mode=selector.NumberSelectorMode.BOX
                        )
                    ),
                }
            ),
        )

    async def async_step_local_options(self, user_input=None):
        """Manage local options."""
        errors = {}
        
        if user_input is not None:
            # Yerel cihaz bağlantısını doğrula
            try:
                device = tinytuya.Device(
                    dev_id=self._config_entry.data[CONF_DEVICE_ID],
                    address=user_input[CONF_IP],
                    local_key=user_input[CONF_LOCAL_KEY],
                    version=float(user_input[CONF_PROTOCOL]),
                )
                status = await self.hass.async_add_executor_job(device.status)
                if not status or 'dps' not in status:
                    errors["base"] = "cannot_connect"
                else:
                    # Güncellemeleri kaydet
                    updated_data = {**self._config_entry.data}
                    updated_data.update({
                        CONF_IP: user_input[CONF_IP],
                        CONF_LOCAL_KEY: user_input[CONF_LOCAL_KEY],
                        CONF_PROTOCOL: user_input[CONF_PROTOCOL],
                    })
                    
                    # ConfigEntry'i güncelle
                    self.hass.config_entries.async_update_entry(
                        self._config_entry,
                        data=updated_data
                    )

                    self._pending_options = {}
                    return await self.async_step_climate_options()
            except Exception:
                _LOGGER.exception("Local validation error in options")
                errors["base"] = "cannot_connect"

        # Mevcut değerleri al
        current_ip = self._config_entry.data.get(CONF_IP, "")
        current_local_key = self._config_entry.data.get(CONF_LOCAL_KEY, "")
        current_protocol = self._config_entry.data.get(CONF_PROTOCOL, "3.4")

        return self.async_show_form(
            step_id="local_options",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_IP, default=current_ip): str,
                    vol.Required(CONF_LOCAL_KEY, default=current_local_key): str,
                    vol.Required(
                        CONF_PROTOCOL, 
                        default=current_protocol
                    ): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=PROTOCOL_OPTIONS,
                            mode=selector.SelectSelectorMode.DROPDOWN
                        )
                    ),
                }
            ),
            errors=errors,
        )

    async def async_step_climate_options(self, user_input=None):
        """Optional climate (thermostat) card — strictly opt-in, default
        off. See const.py's CONF_CLIMATE_* comment for why: most models
        here are pool heat pumps (water is the controlled value, not
        room air) and some already run their own closed-loop room
        control internally, so a second HA-side control loop should
        only exist if the user explicitly asks for it."""
        if user_input is not None:
            self._pending_options = {**self._pending_options, **user_input}
            if user_input.get(CONF_CLIMATE_MODE_SELECT_CODE):
                return await self.async_step_climate_mode_values()
            return self.async_create_entry(title="", data=self._pending_options)

        coordinator = self.hass.data.get(DOMAIN, {}).get(self._config_entry.entry_id)
        model_mapping = coordinator.model_mapping if coordinator else {}

        return self.async_show_form(
            step_id="climate_options",
            data_schema=_climate_options_schema(
                model_mapping, current=self._config_entry.options
            ),
        )

    async def async_step_climate_mode_values(self, user_input=None):
        """Second step, only reached if a mode select was picked above —
        confirm/correct which of ITS real option values means heat and
        which means cool."""
        if user_input is not None:
            self._pending_options = {**self._pending_options, **user_input}
            return self.async_create_entry(title="", data=self._pending_options)

        coordinator = self.hass.data.get(DOMAIN, {}).get(self._config_entry.entry_id)
        model_mapping = coordinator.model_mapping if coordinator else {}
        mode_select_code = self._pending_options.get(CONF_CLIMATE_MODE_SELECT_CODE)
        select_cfg = model_mapping.get("selects", {}).get(mode_select_code, {})

        return self.async_show_form(
            step_id="climate_mode_values",
            data_schema=_climate_mode_values_schema(
                select_cfg, current=self._config_entry.options
            ),
        )


class TuyaHeatpumpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tuya Heat Pump."""

    VERSION = 1
    connection_type = None
    user_data = None  # Geçici user input sakla
    _qr_login = None  # SharingQRLogin instance'ı — bir akış boyunca tek sefer oluşturulur
    _pending_entry_title = None  # climate adımlarına kadar taşınan create_entry bilgisi
    _pending_entry_data = None
    _pending_climate_options = None
    _model_mapping = None  # validate_input'tan gelen, climate dropdown'ları için

    async def async_step_user(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            self.user_data = user_input
            self.connection_type = user_input[CONF_CONNECTION_TYPE]
            if self.connection_type == "cloud":
                return await self.async_step_cloud_options()
            else:
                return await self.async_step_local()

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_cloud_options(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            full_data = {**self.user_data, **user_input}
            self.user_data = full_data  # scan_interval de dahil olacak sekilde guncelle

            # User Code girilmisse (opsiyonel), entry'i hemen olusturmak
            # yerine once QR onayi almamiz lazim.
            if full_data.get(CONF_USER_CODE):
                return await self.async_step_cloud_qr()

            try:
                info = await validate_input(self.hass, full_data, "cloud")
                await self.async_set_unique_id(full_data[CONF_DEVICE_ID])

                # Check if device is already configured
                try:
                    self._abort_if_unique_id_configured()
                except:
                    _LOGGER.error("Device already configured, aborting")
                    return self.async_abort(reason="already_configured")

                self._pending_entry_title = info["title"]
                self._pending_entry_data = full_data
                self._model_mapping = info.get("model_mapping") or {}
                return await self.async_step_climate_options()
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="cloud_options", data_schema=STEP_CLOUD_OPTIONS_SCHEMA, errors=errors
        )

    async def async_step_cloud_qr(self, user_input=None) -> FlowResult:
        """User Code girildiyse buraya düşülür — QR gösterip onay bekler.
        MQTT/tuya_sharing girişi, asıl Access ID/Key ile hiç ilgisi olmayan
        AYRI bir kimlik doğrulama — burada başarısız olsa/atlanırsa bile
        normal cloud kurulumu (periyodik sorgulama) etkilenmez, sadece
        MQTT devreye girmez."""
        errors = {}

        if self._qr_login is None:
            self._qr_login = SharingQRLogin(self.hass)

        if user_input is not None:
            # Kullanici "Confirm" bastiginda buraya dusuyoruz — QR'i
            # onaylamis mi bir kere kontrol ediyoruz (polling degil).
            success, token_info = await self._qr_login.async_check_login(
                self.user_data[CONF_USER_CODE]
            )
            if success and token_info:
                full_data = {**self.user_data, CONF_SHARING_TOKEN_INFO: token_info}
                try:
                    info = await validate_input(self.hass, full_data, "cloud")
                    await self.async_set_unique_id(full_data[CONF_DEVICE_ID])
                    try:
                        self._abort_if_unique_id_configured()
                    except Exception:
                        return self.async_abort(reason="already_configured")

                    self._pending_entry_title = info["title"]
                    self._pending_entry_data = full_data
                    self._model_mapping = info.get("model_mapping") or {}
                    return await self.async_step_climate_options()
                except CannotConnect:
                    errors["base"] = "cannot_connect"
                except InvalidAuth:
                    errors["base"] = "invalid_auth"
                except Exception:
                    _LOGGER.exception("Unexpected exception after QR login")
                    errors["base"] = "unknown"
            else:
                errors["base"] = "qr_not_confirmed"

        # Ilk gosterimde (ya da onay basarisiz olup tekrar denerken) yeni
        # bir QR iste.
        qr_response = await self._qr_login.async_request_qr(self.user_data[CONF_USER_CODE])
        if not qr_response.get("success"):
            _LOGGER.warning("QR kod istegi basarisiz: %s", qr_response)
            errors["base"] = "qr_request_failed"
            schema = vol.Schema({})
        else:
            # HA'nın yerleşik QR selector'ı — tarayıcı QR'ı ham veriden
            # anlık üretiyor, dosya/görsel/data-URI ile uğraşmaya gerek yok.
            schema = vol.Schema(
                {
                    vol.Optional("qr"): selector.QrCodeSelector(
                        config=selector.QrCodeSelectorConfig(
                            data=self._qr_login.qr_token,
                            scale=5,
                            error_correction_level=selector.QrErrorCorrectionLevel.QUARTILE,
                        )
                    )
                }
            )

        return self.async_show_form(
            step_id="cloud_qr",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_local(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            full_data = {**self.user_data, **user_input}
            try:
                info = await validate_input(self.hass, full_data, "local")
                await self.async_set_unique_id(full_data[CONF_DEVICE_ID])

                # Check if device is already configured
                try:
                    self._abort_if_unique_id_configured()
                except:
                    _LOGGER.error("Device already configured, aborting")
                    return self.async_abort(reason="already_configured")

                self._pending_entry_title = info["title"]
                self._pending_entry_data = full_data
                self._model_mapping = info.get("model_mapping") or {}
                return await self.async_step_climate_options()
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="local", data_schema=STEP_LOCAL_DATA_SCHEMA, errors=errors
        )

    async def async_step_climate_options(self, user_input=None) -> FlowResult:
        """Optional climate (thermostat) card, shown at the end of
        initial setup too (not just later in Options) — strictly
        opt-in, default off. See const.py's CONF_CLIMATE_* comment:
        most models here are pool heat pumps (water is the controlled
        value, not room air) and some already run their own closed-loop
        room control internally, so a second HA-side control loop
        should only exist if the user explicitly asks for one."""
        if user_input is not None:
            self._pending_climate_options = dict(user_input)
            if user_input.get(CONF_CLIMATE_MODE_SELECT_CODE):
                return await self.async_step_climate_mode_values()
            return self.async_create_entry(
                title=self._pending_entry_title,
                data=self._pending_entry_data,
                options=self._pending_climate_options,
            )

        return self.async_show_form(
            step_id="climate_options",
            data_schema=_climate_options_schema(self._model_mapping, current={}),
        )

    async def async_step_climate_mode_values(self, user_input=None) -> FlowResult:
        """Second step, only reached if a mode select was picked above —
        confirm/correct which of ITS real option values means heat and
        which means cool."""
        if user_input is not None:
            options = {**self._pending_climate_options, **user_input}
            return self.async_create_entry(
                title=self._pending_entry_title,
                data=self._pending_entry_data,
                options=options,
            )

        mode_select_code = self._pending_climate_options.get(CONF_CLIMATE_MODE_SELECT_CODE)
        select_cfg = (self._model_mapping or {}).get("selects", {}).get(mode_select_code, {})

        return self.async_show_form(
            step_id="climate_mode_values",
            data_schema=_climate_mode_values_schema(select_cfg, current={}),
        )

    @staticmethod
    @config_entries.HANDLERS.register(DOMAIN)
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return TuyaHeatpumpOptionsFlow(config_entry)


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
