"""Climate platform for Tuya Heatpump — optional, user-mapped thermostat card.

Strictly opt-in (default off, see config_flow.py's climate_options step):
most models in this integration are pool heat pumps that target WATER
temperature, not room air, and some models' own Tuya app already runs
closed-loop room-temperature control internally — so unlike every other
platform here, this one creates nothing unless the user has explicitly
picked a power switch (and, optionally, current/target temperature DPs)
for it in the integration's options. The three DPs are plain model_mapping
keys, exactly like switch.py/number.py/sensor.py use — this entity reads
and writes the same coordinator data they do, it is not a wrapper around
other HA entities.
"""
from __future__ import annotations
import logging
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.components.climate.const import ATTR_TEMPERATURE
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    CONF_CLIMATE_ENABLED,
    CONF_CLIMATE_POWER_CODE,
    CONF_CLIMATE_CURRENT_TEMP_CODE,
    CONF_CLIMATE_TARGET_TEMP_CODE,
)
from .conversion import Conversion
from .coordinator import TuyaScaleDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the optional Tuya Heatpump climate entity, if the user has
    enabled it and mapped at least a power switch in Options."""
    options = config_entry.options

    if not options.get(CONF_CLIMATE_ENABLED):
        return

    power_code = options.get(CONF_CLIMATE_POWER_CODE)
    if not power_code:
        _LOGGER.warning(
            "Tuya Heat Pump: climate card is enabled but no power switch "
            "is mapped in Options — skipping, no climate entity created."
        )
        return

    coordinator: TuyaScaleDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    model_mapping = coordinator.model_mapping or {}

    power_config = model_mapping.get("switches", {}).get(power_code)
    if power_config is None:
        _LOGGER.warning(
            "Tuya Heat Pump: climate power code '%s' is no longer present "
            "in this model's mapping — skipping, no climate entity created.",
            power_code,
        )
        return

    current_code = options.get(CONF_CLIMATE_CURRENT_TEMP_CODE) or None
    current_config = None
    if current_code:
        current_config = model_mapping.get("sensors", {}).get(current_code) or \
            model_mapping.get("numbers", {}).get(current_code)
        if current_config is None:
            current_code = None

    target_code = options.get(CONF_CLIMATE_TARGET_TEMP_CODE) or None
    target_config = None
    if target_code:
        target_config = model_mapping.get("numbers", {}).get(target_code)
        if target_config is None:
            target_code = None

    async_add_entities([
        TuyaHeatpumpClimate(
            coordinator,
            power_code, power_config,
            current_code, current_config,
            target_code, target_config,
        )
    ])
    _LOGGER.info(
        "Adding climate entity (power=%s, current=%s, target=%s)",
        power_code, current_code, target_code,
    )


class TuyaHeatpumpClimate(ClimateEntity):
    """A simple on/off (+ optional target-temperature) climate card,
    built from the same plain DP codes switch.py/sensor.py/number.py
    already expose for this model."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
    _attr_temperature_unit = UnitOfTemperature.CELSIUS

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        power_code: str, power_config: dict,
        current_code: str | None, current_config: dict | None,
        target_code: str | None, target_config: dict | None,
    ) -> None:
        """Initialize the climate entity."""
        self.coordinator = coordinator
        self._power_code = power_code
        self._power_config = power_config or {}
        self._current_code = current_code
        self._current_config = current_config or {}
        self._target_code = target_code
        self._target_config = target_config or {}

        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_climate"

        # Device info
        self._attr_device_info = coordinator.device_info

        features = ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF
        if target_code:
            features |= ClimateEntityFeature.TARGET_TEMPERATURE
            self._attr_target_temperature_step = self._target_config.get("step", 1)
            if "min_value" in self._target_config:
                self._attr_min_temp = self._target_config["min_value"]
            if "max_value" in self._target_config:
                self._attr_max_temp = self._target_config["max_value"]
        self._attr_supported_features = features

    def _resolve_code(self, code: str, config: dict) -> str:
        """The real Tuya DP code to use for coordinator.data lookups and
        for send_command (normally identical to the dict key, but a
        model file can set an explicit "code" to decouple the two —
        see binary_sensor.py's identical helper)."""
        return config.get("code", code)

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info

    def _read_bool(self, code: str, config: dict) -> bool | None:
        if not self.coordinator.data or code not in self.coordinator.data:
            return None
        raw_value = self.coordinator.data[code]["value"]
        conversion = Conversion(config.get("conversion", "bool(value)"))
        try:
            return bool(conversion.convert(raw_value))
        except Exception as err:
            _LOGGER.warning("Conversion failed for climate power (%s): %s", code, err)
            if isinstance(raw_value, bool):
                return raw_value
            if isinstance(raw_value, (int, float)):
                return bool(raw_value)
            if isinstance(raw_value, str):
                return raw_value.lower() in ("true", "1", "on", "yes", "enable", "open")
            return None

    def _read_float(self, code: str, config: dict) -> float | None:
        if not self.coordinator.data or code not in self.coordinator.data:
            return None
        raw_value = self.coordinator.data[code]["value"]
        conversion = Conversion(config.get("conversion", "value"))
        try:
            result = conversion.convert(raw_value)
            return float(result) if isinstance(result, (int, float)) else None
        except Exception as err:
            _LOGGER.warning("Conversion failed for climate temperature (%s): %s", code, err)
            try:
                return float(raw_value)
            except (TypeError, ValueError):
                return None

    @property
    def hvac_mode(self) -> HVACMode:
        """Return current HVAC mode, based on the mapped power switch."""
        is_on = self._read_bool(
            self._resolve_code(self._power_code, self._power_config), self._power_config
        )
        return HVACMode.HEAT if is_on else HVACMode.OFF

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return current HVAC action, based on the mapped power switch."""
        is_on = self._read_bool(
            self._resolve_code(self._power_code, self._power_config), self._power_config
        )
        if is_on is None:
            return None
        return HVACAction.HEATING if is_on else HVACAction.OFF

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature, from the mapped DP (if any)."""
        if not self._current_code:
            return None
        return self._read_float(
            self._resolve_code(self._current_code, self._current_config), self._current_config
        )

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature, from the mapped DP (if any)."""
        if not self._target_code:
            return None
        return self._read_float(
            self._resolve_code(self._target_code, self._target_config), self._target_config
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Tuya DP ID ve Code bilgilerini attributes'a ekle."""
        attrs: dict[str, Any] = {}

        power_lookup = self._resolve_code(self._power_code, self._power_config)
        dp_info = self.coordinator.get_tuya_dp_info(power_lookup)
        attrs["tuya_power_code"] = dp_info["code"]
        attrs["tuya_power_dp_id"] = dp_info["dp_id"]

        if self._current_code:
            attrs["tuya_current_temp_code"] = self._resolve_code(
                self._current_code, self._current_config
            )
        if self._target_code:
            attrs["tuya_target_temp_code"] = self._resolve_code(
                self._target_code, self._target_config
            )

        if self.coordinator.model_id:
            attrs["tuya_model_id"] = self.coordinator.model_id

        return attrs

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        lookup_code = self._resolve_code(self._power_code, self._power_config)
        return (
            self.coordinator.last_update_success
            and self.coordinator.data is not None
            and lookup_code in self.coordinator.data
        )

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Turn the mapped power switch on/off."""
        _LOGGER.info("Setting climate HVAC mode to %s", hvac_mode)

        api_value = hvac_mode == HVACMode.HEAT
        if (api_conversion := self._power_config.get("api_conversion")) is not None:
            conversion = Conversion(api_conversion)
            try:
                api_value = conversion.convert(api_value)
            except Exception as err:
                _LOGGER.warning("API conversion failed for climate power: %s", err)

        success = await self.coordinator.send_command(
            self._resolve_code(self._power_code, self._power_config), api_value
        )

        if success:
            _LOGGER.info("✅ Successfully set climate HVAC mode to %s", hvac_mode)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.warning("❌ Failed to set climate HVAC mode to %s", hvac_mode)
            raise HomeAssistantError("Could not change the heat pump's power state.")

    async def async_turn_on(self) -> None:
        """Turn the heat pump on."""
        await self.async_set_hvac_mode(HVACMode.HEAT)

    async def async_turn_off(self) -> None:
        """Turn the heat pump off."""
        await self.async_set_hvac_mode(HVACMode.OFF)

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set a new target temperature."""
        if not self._target_code:
            raise HomeAssistantError(
                "This device has no target-temperature field mapped — "
                "set one in the integration's options, if your device has one."
            )

        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        _LOGGER.info("Attempting to set climate target temperature to %s", temperature)

        api_value = temperature
        if (api_conversion := self._target_config.get("api_conversion")) is not None:
            conversion = Conversion(api_conversion)
            try:
                api_value = conversion.convert(temperature)
            except Exception as err:
                _LOGGER.warning("API conversion failed for climate target: %s", err)

        success = await self.coordinator.send_command(
            self._resolve_code(self._target_code, self._target_config),
            api_value,
            display_value=temperature,
        )

        if success:
            _LOGGER.info("✅ Successfully set climate target temperature to %s", temperature)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.warning("❌ Failed to set climate target temperature to %s", temperature)
            raise HomeAssistantError(
                "Could not change the target temperature. Your device may not "
                "allow changing this setting remotely."
            )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
