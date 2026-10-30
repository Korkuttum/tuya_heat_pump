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
    CONF_AUTH_METHOD,
    AUTH_METHOD_ACCESS_KEY,
    AUTH_METHOD_SHARING,
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
from .sharing_mqtt import SharingQRLogin, SharingMQTT, async_build_manager
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

    # Min/max always apply (direct or virtual mode alike -- climate.py no
    # longer locks them to the device's own reported range, since some
    # model files only have a generic placeholder like 0-100). Here they
    # just get a sensible SUGGESTED default: the currently-selected
    # target DP's own min/max if it has one, otherwise the generic
    # DEFAULT_CLIMATE_*_TEMP constants -- always editable either way.
    current_target_code = current.get(CONF_CLIMATE_TARGET_TEMP_CODE) or defaults.get("target", "")
    target_cfg_for_range = model_mapping.get("numbers", {}).get(current_target_code, {})
    suggested_min_temp = target_cfg_for_range.get("min_value", DEFAULT_CLIMATE_MIN_TEMP)
    suggested_max_temp = target_cfg_for_range.get("max_value", DEFAULT_CLIMATE_MAX_TEMP)

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
                default=current.get(CONF_CLIMATE_MIN_TEMP, suggested_min_temp),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=-20, max=100, step=1, mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="°C",
                )
            ),
            vol.Optional(
                CONF_CLIMATE_MAX_TEMP,
                default=current.get(CONF_CLIMATE_MAX_TEMP, suggested_max_temp),
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

def _scan_for_device_ip(device_id: str) -> str | None:
    """tinytuya'nın LAN broadcast taramasıyla bu device_id'nin şu anki
    gerçek yerel IP'sini bulmaya çalışır. Sharing session'ın kendi
    `ip` alanı KULLANILAMAZ -- bu Tuya cloud'un gördüğü WAN/genel IP,
    yerel ağ adresi değil (canlı testte doğrulandı: o IP'ye direkt
    bağlanma denemesi "Device Unreachable" veriyor). Senkron ve birkaç
    saniye sürebilir -- çağıran taraf executor job içinde çalıştırmalı."""
    try:
        found = tinytuya.deviceScan(verbose=False, poll=False)
    except Exception as err:
        _LOGGER.debug("LAN taraması başarısız: %s", err)
        return None
    for ip, info in found.items():
        if info.get("gwId") == device_id or info.get("id") == device_id:
            return ip
    return None


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

    if connection_type == "cloud" and coordinator.auth_method == AUTH_METHOD_SHARING:
        # Access ID/Key yok -- _get_token()/get_device_info()'nun eski
        # imzalı-istek mantığı burada hiç çağrılamaz (access_id None
        # olduğu için "unsupported operand type(s) for +=: 'NoneType'
        # and 'str'" ile çöker, bkz. coordinator._calculate_sign).
        # Bunun yerine sharing oturumunun GERÇEKTEN kurulabildiğini
        # doğruluyoruz -- bu, get_device_model()'in kendi (başarısız
        # olursa sessizce "default"a düşen) best-effort denemesinden
        # FARKLI: burada başarısızlık CannotConnect olarak fırlatılmalı,
        # yoksa kurulum, bağlanamayan bir cihazla sessizce tamamlanır.
        try:
            if coordinator.sharing_mqtt is None:
                coordinator.sharing_mqtt = SharingMQTT(hass, coordinator)
            if not await coordinator.sharing_mqtt.async_connect():
                raise CannotConnect("Sharing oturumu kurulamadı")
        except CannotConnect:
            raise
        except Exception as err:
            _LOGGER.error("Sharing validation error: %s", err)
            raise CannotConnect("Cannot connect via sharing session") from err

        title = f"Tuya Heat Pump ({data[CONF_DEVICE_ID]})"

    elif connection_type == "cloud":
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

    _qr_login = None  # SharingQRLogin instance'ı — switch_to_sharing akışı için
    _sharing_user_code = None

    def __init__(self, config_entry):
        """Initialize options flow."""
        self._config_entry = config_entry
        self.connection_type = config_entry.data.get(CONF_CONNECTION_TYPE, "cloud")
        self._pending_options: dict = {}

    async def async_step_init(self, user_input=None):
        """Top-level menu — connection settings and the optional climate
        card are independent sections now: editing one never touches or
        re-asks about the other (previously connection settings silently
        chained into climate questions every time, and saving local
        connection details could wipe out already-saved climate options).

        v3.0.0: Cloud + auth_method="access_key" kurulumlara (hem eski
        hem yeni) bir üçüncü seçenek eklendi -- "QR'a geç": #111'de
        konuşulan "mevcut cloud kurulumuna sonradan MQTT ekleme"
        ihtiyacını da aynı anda çözüyor, çünkü sharing'e geçince MQTT
        zaten otomatik gelir."""
        menu_options = ["connection_options", "climate_options"]
        auth_method = self._config_entry.data.get(CONF_AUTH_METHOD, AUTH_METHOD_ACCESS_KEY)
        if auth_method == AUTH_METHOD_ACCESS_KEY and self.connection_type == "cloud":
            menu_options.append("switch_to_sharing")
        return self.async_show_menu(
            step_id="init",
            menu_options=menu_options,
        )

    async def async_step_switch_to_sharing(self, user_input=None):
        """Mevcut Cloud+Access-ID/Key kurulumunu auth_method="sharing"'e
        çevirir -- device_id SABİT kalır (zaten biliniyor, yeniden
        seçtirmeye gerek yok), sadece User Code + QR isteniyor."""
        errors = {}
        if user_input is not None:
            self._sharing_user_code = user_input[CONF_USER_CODE]
            return await self.async_step_switch_to_sharing_qr()

        return self.async_show_form(
            step_id="switch_to_sharing",
            data_schema=vol.Schema({vol.Required(CONF_USER_CODE): str}),
            errors=errors,
        )

    async def async_step_switch_to_sharing_qr(self, user_input=None):
        """QR göster, onay bekle. Başarılıysa entry.data'yı auth_method=
        sharing'e çevirip reload tetikler -- coordinator bir dahaki
        kurulumda (zaten cached_model_id varsa model tespitini tekrar
        yapmadan) _async_start_mqtt() üzerinden sharing oturumunu
        kendisi kurar."""
        errors = {}
        if self._qr_login is None:
            self._qr_login = SharingQRLogin(self.hass)

        if user_input is not None:
            success, token_info = await self._qr_login.async_check_login(
                self._sharing_user_code
            )
            if success and token_info:
                updated_data = {
                    **self._config_entry.data,
                    CONF_AUTH_METHOD: AUTH_METHOD_SHARING,
                    CONF_USER_CODE: self._sharing_user_code,
                    CONF_SHARING_TOKEN_INFO: token_info,
                }
                self.hass.config_entries.async_update_entry(
                    self._config_entry, data=updated_data
                )
                # Sadece entry.data değişti, options aynı kalıyor --
                # climate ayarları (varsa) dokunulmadan korunuyor.
                return self.async_create_entry(title="", data=dict(self._config_entry.options))
            errors["base"] = "qr_not_confirmed"

        qr_response = await self._qr_login.async_request_qr(self._sharing_user_code)
        if not qr_response.get("success"):
            errors["base"] = "qr_request_failed"
            schema = vol.Schema({})
        else:
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
            step_id="switch_to_sharing_qr", data_schema=schema, errors=errors
        )

    async def async_step_connection_options(self, user_input=None):
        """Route to the cloud/local connection settings form."""
        if self.connection_type == "cloud":
            return await self.async_step_cloud_options()
        else:
            return await self.async_step_local_options()

    async def async_step_cloud_options(self, user_input=None):
        """Manage cloud options."""
        if user_input is not None:
            data = {**self._config_entry.options, **user_input}
            return self.async_create_entry(title="", data=data)

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

                    # Bu adım sadece bağlantı bilgilerini (entry.data)
                    # değiştiriyor — entry.options'a (climate ayarları
                    # dahil) hiç dokunmamalı, olduğu gibi korunmalı.
                    return self.async_create_entry(title="", data=dict(self._config_entry.options))
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
            data = {**self._config_entry.options, **user_input}
            # Sadece gerçekten etkinleştirilmişse VE bir mode-select
            # seçilmişse heat/cool sorusuna geç — kapatırken (enabled
            # False) dropdown'daki eski değer hâlâ dolu olsa bile bir
            # daha sormamalı.
            if user_input.get(CONF_CLIMATE_ENABLED) and user_input.get(CONF_CLIMATE_MODE_SELECT_CODE):
                self._pending_options = data
                return await self.async_step_climate_mode_values()
            return self.async_create_entry(title="", data=data)

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
            data = {**self._pending_options, **user_input}
            return self.async_create_entry(title="", data=data)

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

    # --- v3.0.0: "sharing" (User Code + QR, Access ID/Key'e gerek yok)
    # kurulum akışı boyunca taşınan geçici durum. Bkz. async_step_setup_
    # sharing ve devamındaki adımlar.
    _sharing_user_code = None
    _sharing_token_info = None
    _sharing_manager = None  # tuya_sharing.Manager -- cihaz listesi için
    _sharing_device_id = None
    _sharing_local_key = None

    async def async_step_user(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """İlk ekran: yeni, basit yol (sadece User Code + QR, Access
        ID/Key'e hiç gerek yok) önce gösteriliyor -- kullanıcıyı buna
        yönlendiriyoruz. Eski Access ID/Key yolu hâlâ burada, kaldırılmadı."""
        return self.async_show_menu(
            step_id="user",
            menu_options=["setup_sharing", "setup_access_key"],
        )

    async def async_step_setup_access_key(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Eski yöntemin tamamı — eski async_step_user'ın içeriği,
        davranışı hiç değişmedi."""
        errors = {}

        if user_input is not None:
            self.user_data = {**user_input, CONF_AUTH_METHOD: AUTH_METHOD_ACCESS_KEY}
            self.connection_type = user_input[CONF_CONNECTION_TYPE]
            if self.connection_type == "cloud":
                return await self.async_step_cloud_options()
            else:
                return await self.async_step_local()

        return self.async_show_form(
            step_id="setup_access_key", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    # ============================================================================
    # v3.0.0: "sharing" kurulum akışı (sadece User Code + QR) — yeni, önerilen yol
    # ============================================================================

    async def async_step_setup_sharing(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """User Code iste — QR'a geçmeden önceki ilk adım."""
        errors = {}
        if user_input is not None:
            self._sharing_user_code = user_input[CONF_USER_CODE]
            return await self.async_step_sharing_qr()

        return self.async_show_form(
            step_id="setup_sharing",
            data_schema=vol.Schema({vol.Required(CONF_USER_CODE): str}),
            errors=errors,
        )

    async def async_step_sharing_qr(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """QR göster, onay bekle. Başarılıysa (async_step_cloud_qr'ın
        aksine) doğrudan entry oluşturmaya geçmiyoruz -- önce bu hesabın
        TÜM cihazlarını listeleyip kullanıcıya seçtiriyoruz (bkz.
        async_step_sharing_device_pick)."""
        errors = {}

        if self._qr_login is None:
            self._qr_login = SharingQRLogin(self.hass)

        if user_input is not None:
            success, token_info = await self._qr_login.async_check_login(
                self._sharing_user_code
            )
            if success and token_info:
                self._sharing_token_info = token_info
                try:
                    self._sharing_manager = await async_build_manager(
                        self.hass, self._sharing_user_code, token_info
                    )
                except Exception:
                    _LOGGER.exception("Sharing: Manager kurulamadı")
                    errors["base"] = "unknown"
                else:
                    return await self.async_step_sharing_device_pick()
            else:
                errors["base"] = "qr_not_confirmed"

        qr_response = await self._qr_login.async_request_qr(self._sharing_user_code)
        if not qr_response.get("success"):
            _LOGGER.warning("QR kod istegi basarisiz: %s", qr_response)
            errors["base"] = "qr_request_failed"
            schema = vol.Schema({})
        else:
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
            step_id="sharing_qr",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_sharing_device_pick(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Hesaptaki TÜM cihazları listele (sadece ısı pompaları değil --
        hangi cihazın ısı pompası olduğunu kategori adından biz
        bilemeyiz, kullanıcı kendi seçsin)."""
        errors = {}
        devices = self._sharing_manager.device_map if self._sharing_manager else {}

        if not devices:
            return self.async_abort(reason="no_devices_found")

        if user_input is not None:
            device_id = user_input[CONF_DEVICE_ID]
            device = devices.get(device_id)
            if device is None:
                errors["base"] = "unknown"
            else:
                self._sharing_device_id = device_id
                self._sharing_local_key = getattr(device, "local_key", None)
                return await self.async_step_sharing_connection_type()

        options = [
            selector.SelectOptionDict(
                value=device_id,
                label=f"{getattr(device, 'name', device_id)} ({getattr(device, 'category', '?')})",
            )
            for device_id, device in devices.items()
        ]
        schema = vol.Schema(
            {
                vol.Required(CONF_DEVICE_ID): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=options, mode=selector.SelectSelectorMode.DROPDOWN
                    )
                )
            }
        )
        return self.async_show_form(
            step_id="sharing_device_pick", data_schema=schema, errors=errors
        )

    async def async_step_sharing_connection_type(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Local mi Cloud mu? Cloud ise bu AYNI oturum durum okuma/komut/
        push için kullanılır (Access ID/Key yok); Local ise sadece
        local_key (zaten elimizde) + IP (sıradaki adımda LAN taraması)
        için kullanıldı, asıl kontrol tinytuya ile olacak."""
        if user_input is not None:
            self.connection_type = user_input[CONF_CONNECTION_TYPE]
            if self.connection_type == "cloud":
                return await self._finish_sharing_cloud()
            return await self.async_step_sharing_local_ip()

        schema = vol.Schema(
            {
                vol.Required(CONF_CONNECTION_TYPE, default="cloud"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(
                                value="cloud",
                                label="Cloud (status/commands/push over this same session)",
                            ),
                            selector.SelectOptionDict(
                                value="local",
                                label="Local (direct LAN control — faster, no internet needed after setup)",
                            ),
                        ],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                )
            }
        )
        return self.async_show_form(step_id="sharing_connection_type", data_schema=schema)

    async def async_step_sharing_local_ip(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """local_key zaten elimizde (sharing oturumundan) -- sadece IP
        gerekiyor. Önce tinytuya'nın LAN broadcast taramasıyla otomatik
        bulmayı deniyoruz (sharing oturumunun kendi `ip` alanı WAN/genel
        IP, kullanılamaz -- canlı testte doğrulandı); bulunamazsa
        kullanıcı elle giriyor."""
        errors = {}

        if user_input is not None:
            full_data = {
                CONF_DEVICE_ID: self._sharing_device_id,
                CONF_AUTH_METHOD: AUTH_METHOD_SHARING,
                CONF_CONNECTION_TYPE: "local",
                CONF_IP: user_input[CONF_IP],
                CONF_LOCAL_KEY: self._sharing_local_key,
                CONF_PROTOCOL: user_input[CONF_PROTOCOL],
                CONF_USER_CODE: self._sharing_user_code,
                CONF_SHARING_TOKEN_INFO: self._sharing_token_info,
            }
            try:
                info = await validate_input(self.hass, full_data, "local")
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
            except Exception:
                _LOGGER.exception("Unexpected exception (sharing local)")
                errors["base"] = "unknown"

        scanned_ip = await self.hass.async_add_executor_job(
            _scan_for_device_ip, self._sharing_device_id
        )
        ip_field = (
            vol.Required(CONF_IP, default=scanned_ip)
            if scanned_ip
            else vol.Required(CONF_IP)
        )
        schema = vol.Schema(
            {
                ip_field: str,
                vol.Required(CONF_PROTOCOL, default="3.4"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=PROTOCOL_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )
        return self.async_show_form(
            step_id="sharing_local_ip",
            data_schema=schema,
            errors=errors,
            description_placeholders={
                "scan_result": scanned_ip or "not found automatically — please enter it manually"
            },
        )

    async def _finish_sharing_cloud(self) -> FlowResult:
        """Cloud yolunda IP/local_key'e hiç ihtiyaç yok -- doğrudan
        validate_input'a geçiyoruz (aynı mock-coordinator mekanizması,
        auth_method="sharing" sayesinde coordinator.get_device_model()
        otomatik olarak doğru dalı seçiyor)."""
        full_data = {
            CONF_DEVICE_ID: self._sharing_device_id,
            CONF_AUTH_METHOD: AUTH_METHOD_SHARING,
            CONF_CONNECTION_TYPE: "cloud",
            CONF_USER_CODE: self._sharing_user_code,
            CONF_SHARING_TOKEN_INFO: self._sharing_token_info,
            CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
        }
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
            return self.async_abort(reason="cannot_connect")
        except Exception:
            _LOGGER.exception("Unexpected exception (sharing cloud)")
            return self.async_abort(reason="unknown")

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
            # Sadece gerçekten etkinleştirilmişse VE bir mode-select
            # seçilmişse heat/cool sorusuna geç.
            if user_input.get(CONF_CLIMATE_ENABLED) and user_input.get(CONF_CLIMATE_MODE_SELECT_CODE):
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
