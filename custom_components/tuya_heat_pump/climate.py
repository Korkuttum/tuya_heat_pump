"""Climate platform for Tuya Heatpump — optional, user-mapped thermostat card.

Strictly opt-in (default off, see config_flow.py's climate_options step):
most models in this integration are pool heat pumps that target WATER
temperature, not room air, and some models' own Tuya app already runs
closed-loop room-temperature control internally — so unlike every other
platform here, this one creates nothing unless the user has explicitly
picked a power switch for it in Options.

Two sub-modes, chosen automatically from what the user mapped (not a
separate toggle):

- "Direct": a real, writable target-temperature DP was picked. The card
  writes straight to that DP — the device already runs its own closed
  control loop, we are just a UI for it. No hysteresis logic needed.
- "Virtual": no target DP was picked (but a current-temperature DP was).
  The card behaves like Home Assistant's own generic_thermostat: the
  target temperature is kept in HA only (restored across restarts) and
  the mapped power switch is driven by a simple current-vs-target
  hysteresis loop, gated by a minimum cycle duration to protect the
  compressor from short-cycling.

An optional mode-select DP (the repo's "work_mode"-style SELECT_TYPES
entry) adds HVACMode.COOL alongside HEAT, for heat pumps that can also
cool.
"""
from __future__ import annotations
import logging
from datetime import timedelta
from typing import Any

import homeassistant.util.dt as dt_util
from homeassistant.components.climate import (
    ATTR_TEMPERATURE,
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    DOMAIN,
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

    mode_select_code = options.get(CONF_CLIMATE_MODE_SELECT_CODE) or None
    mode_select_config = None
    heat_value = options.get(CONF_CLIMATE_HEAT_VALUE) or None
    cool_value = options.get(CONF_CLIMATE_COOL_VALUE) or None
    if mode_select_code:
        mode_select_config = model_mapping.get("selects", {}).get(mode_select_code)
        if mode_select_config is None or not heat_value or not cool_value:
            mode_select_code = None
            mode_select_config = None
            heat_value = None
            cool_value = None

    tolerance = options.get(CONF_CLIMATE_TOLERANCE, DEFAULT_CLIMATE_TOLERANCE)
    min_cycle_minutes = options.get(CONF_CLIMATE_MIN_CYCLE_MINUTES, DEFAULT_CLIMATE_MIN_CYCLE_MINUTES)
    min_temp = options.get(CONF_CLIMATE_MIN_TEMP, DEFAULT_CLIMATE_MIN_TEMP)
    max_temp = options.get(CONF_CLIMATE_MAX_TEMP, DEFAULT_CLIMATE_MAX_TEMP)

    async_add_entities([
        TuyaHeatpumpClimate(
            coordinator,
            power_code, power_config,
            current_code, current_config,
            target_code, target_config,
            mode_select_code, mode_select_config, heat_value, cool_value,
            tolerance, min_cycle_minutes, min_temp, max_temp,
        )
    ])
    _LOGGER.info(
        "Adding climate entity (power=%s, current=%s, target=%s, mode_select=%s)",
        power_code, current_code, target_code, mode_select_code,
    )


class TuyaHeatpumpClimate(ClimateEntity, RestoreEntity):
    """A climate card built from the same plain DP codes
    switch.py/sensor.py/number.py/select.py already expose for this model."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_temperature_unit = UnitOfTemperature.CELSIUS

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        power_code: str, power_config: dict,
        current_code: str | None, current_config: dict | None,
        target_code: str | None, target_config: dict | None,
        mode_select_code: str | None, mode_select_config: dict | None,
        heat_value: str | None, cool_value: str | None,
        tolerance: float, min_cycle_minutes: float,
        min_temp: float, max_temp: float,
    ) -> None:
        """Initialize the climate entity."""
        self.coordinator = coordinator
        self._power_code = power_code
        self._power_config = power_config or {}
        self._current_code = current_code
        self._current_config = current_config or {}
        self._target_code = target_code
        self._target_config = target_config or {}
        self._mode_select_code = mode_select_code
        self._mode_select_config = mode_select_config or {}
        self._heat_value = heat_value
        self._cool_value = cool_value
        self._tolerance = tolerance
        self._min_cycle_duration = timedelta(minutes=min_cycle_minutes) if min_cycle_minutes else None

        # "Virtual" mode: no real device target, but a current-temperature
        # reading exists to drive a local hysteresis loop against. Set
        # (target_code present) always wins — the device already runs its
        # own closed loop there, so no hysteresis is needed or wanted.
        self._is_virtual = self._target_code is None and self._current_code is not None
        self._hvac_mode: HVACMode = HVACMode.OFF
        # Remembers the last non-OFF mode the user explicitly picked, so
        # the simple power-on toggle (async_turn_on) can resume HEAT or
        # COOL correctly instead of always forcing HEAT.
        self._last_active_mode: HVACMode = HVACMode.HEAT
        self._virtual_target_temperature: float | None = None
        self._last_power_change = None

        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_climate"
        self._attr_device_info = coordinator.device_info

        hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
        if self._mode_select_code and self._heat_value and self._cool_value:
            hvac_modes = [HVACMode.HEAT, HVACMode.COOL, HVACMode.OFF]
        self._attr_hvac_modes = hvac_modes

        features = ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF
        has_target_control = bool(self._target_code) or bool(self._current_code)
        if has_target_control:
            features |= ClimateEntityFeature.TARGET_TEMPERATURE
        self._attr_supported_features = features

        # Min/max always come from Options (pre-filled there from the
        # device's own reported range when a target is picked, but the
        # user can override it either way — some model files only have a
        # generic placeholder range, e.g. 0-100, that isn't the real
        # usable range for that specific device). Only the step stays
        # tied to the device's own real hardware increment in direct mode.
        self._attr_min_temp = min_temp
        self._attr_max_temp = max_temp
        if self._target_code:
            self._attr_target_temperature_step = self._target_config.get("step", 1)
        else:
            self._attr_target_temperature_step = 0.5

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

    def _read_select_raw(self, code: str, config: dict) -> str | None:
        """The raw Tuya enum value currently reported for a SELECT_TYPES
        DP (not the human-readable label select.py shows in the UI)."""
        if not self.coordinator.data or code not in self.coordinator.data:
            return None
        raw_value = self.coordinator.data[code]["value"]
        conversion = Conversion(config.get("conversion", "value"))
        try:
            value = conversion.convert(raw_value)
        except Exception:
            value = raw_value
        return value if isinstance(value, str) else None

    @property
    def hvac_mode(self) -> HVACMode:
        """Return current HVAC mode."""
        if self._is_virtual:
            return self._hvac_mode

        is_on = self._read_bool(
            self._resolve_code(self._power_code, self._power_config), self._power_config
        )
        if not is_on:
            return HVACMode.OFF
        if self._mode_select_code:
            current_raw = self._read_select_raw(
                self._resolve_code(self._mode_select_code, self._mode_select_config),
                self._mode_select_config,
            )
            if current_raw == self._cool_value:
                return HVACMode.COOL
        return HVACMode.HEAT

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return current HVAC action."""
        if self._is_virtual:
            if self._hvac_mode == HVACMode.OFF:
                return HVACAction.OFF
            is_on = self._read_bool(
                self._resolve_code(self._power_code, self._power_config), self._power_config
            )
            if is_on is None:
                return None
            if not is_on:
                return HVACAction.IDLE
            return HVACAction.COOLING if self._hvac_mode == HVACMode.COOL else HVACAction.HEATING

        is_on = self._read_bool(
            self._resolve_code(self._power_code, self._power_config), self._power_config
        )
        if is_on is None:
            return None
        if not is_on:
            return HVACAction.OFF
        return HVACAction.COOLING if self.hvac_mode == HVACMode.COOL else HVACAction.HEATING

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
        """Return the target temperature."""
        if self._target_code:
            return self._read_float(
                self._resolve_code(self._target_code, self._target_config), self._target_config
            )
        return self._virtual_target_temperature

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
        if self._mode_select_code:
            attrs["tuya_mode_select_code"] = self._resolve_code(
                self._mode_select_code, self._mode_select_config
            )
            attrs["tuya_heat_value"] = self._heat_value
            attrs["tuya_cool_value"] = self._cool_value

        attrs["climate_bridge_mode"] = "direct" if self._target_code else (
            "virtual" if self._is_virtual else "power_only"
        )
        if self._is_virtual:
            # Restored across restarts (see async_added_to_hass) so the
            # power-on toggle can resume the right mode.
            attrs["last_active_mode"] = self._last_active_mode.value

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

    async def _async_power(self, on: bool, *, respect_min_cycle: bool = True) -> None:
        """Turn the mapped power switch on/off, optionally gated by the
        minimum cycle duration (compressor short-cycling protection)."""
        now = dt_util.utcnow()
        if respect_min_cycle and self._min_cycle_duration and self._last_power_change is not None:
            if now - self._last_power_change < self._min_cycle_duration:
                _LOGGER.debug(
                    "Climate: skipping automatic power change, minimum cycle "
                    "duration hasn't elapsed yet"
                )
                return

        api_value = on
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
            self._last_power_change = now
            await self.coordinator.async_request_refresh()
        else:
            raise HomeAssistantError("Could not change the heat pump's power state.")

    async def _async_set_mode_select(self, raw_value: str) -> None:
        """Write the mapped heat/cool mode-select DP to one of its own
        raw values (not the human-readable label)."""
        if not self._mode_select_code:
            return

        api_value = raw_value
        if (api_conversion := self._mode_select_config.get("api_conversion")) is not None:
            conversion = Conversion(api_conversion)
            try:
                api_value = conversion.convert(raw_value)
            except Exception as err:
                _LOGGER.warning("API conversion failed for climate mode select: %s", err)

        success = await self.coordinator.send_command(
            self._resolve_code(self._mode_select_code, self._mode_select_config), api_value
        )
        if not success:
            raise HomeAssistantError("Could not change the heat pump's heat/cool mode.")

    async def _async_control_heating(self, *, force: bool = False) -> None:
        """Virtual-mode hysteresis: drive the power switch from current
        vs target, direction depending on the active hvac_mode. No-op in
        direct mode — the device runs its own closed loop there."""
        if not self._is_virtual or self._hvac_mode == HVACMode.OFF:
            return

        current = self.current_temperature
        target = self.target_temperature
        if current is None or target is None:
            return

        is_on = self._read_bool(
            self._resolve_code(self._power_code, self._power_config), self._power_config
        )
        if is_on is None:
            return

        if self._hvac_mode == HVACMode.COOL:
            should_run = current >= target + self._tolerance
            should_stop = current <= target - self._tolerance
        else:
            should_run = current <= target - self._tolerance
            should_stop = current >= target + self._tolerance

        if should_run and not is_on:
            await self._async_power(True, respect_min_cycle=not force)
        elif should_stop and is_on:
            await self._async_power(False, respect_min_cycle=not force)

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set a new HVAC mode."""
        _LOGGER.info("Setting climate HVAC mode to %s", hvac_mode)

        if hvac_mode != HVACMode.OFF:
            self._last_active_mode = hvac_mode

        if self._is_virtual:
            self._hvac_mode = hvac_mode
            self.async_write_ha_state()
            if hvac_mode == HVACMode.OFF:
                await self._async_power(False, respect_min_cycle=False)
            else:
                if hvac_mode == HVACMode.COOL and self._cool_value:
                    await self._async_set_mode_select(self._cool_value)
                elif hvac_mode == HVACMode.HEAT and self._mode_select_code and self._heat_value:
                    await self._async_set_mode_select(self._heat_value)
                await self._async_control_heating(force=True)
            return

        # Direct mode: hvac_mode maps straight onto the power switch (+
        # the mode-select, if the device has a heat/cool mode mapped).
        if hvac_mode == HVACMode.OFF:
            await self._async_power(False)
            return

        if hvac_mode == HVACMode.COOL and self._cool_value:
            await self._async_set_mode_select(self._cool_value)
        elif hvac_mode == HVACMode.HEAT and self._mode_select_code and self._heat_value:
            await self._async_set_mode_select(self._heat_value)

        await self._async_power(True)

    async def async_turn_on(self) -> None:
        """Turn the heat pump on, resuming its last heat/cool mode."""
        if self._is_virtual:
            # Virtual mode tracks its own mode locally (there is no
            # device state to read it back from), so resume explicitly.
            await self.async_set_hvac_mode(self._last_active_mode)
        else:
            # Direct mode: the device itself remembers its own last
            # heat/cool mode-select value even while off, so just flip
            # power — rewriting the mode here would be redundant, and
            # async_set_hvac_mode(HEAT) would wrongly force HEAT even if
            # the device was last in COOL.
            await self._async_power(True)

    async def async_turn_off(self) -> None:
        """Turn the heat pump off."""
        await self.async_set_hvac_mode(HVACMode.OFF)

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set a new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        if self._target_code:
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
            return

        if not self._is_virtual:
            raise HomeAssistantError(
                "This device has no target-temperature field mapped — "
                "set one in the integration's options, if your device has one."
            )

        # Virtual mode: the target lives in HA only, the hysteresis loop
        # does the rest.
        self._virtual_target_temperature = temperature
        self.async_write_ha_state()
        await self._async_control_heating()

    async def _async_control_heating_safe(self) -> None:
        """Background-triggered control pass — log and move on instead of
        raising into an unretrieved task exception (unlike a direct user
        action, nobody is watching this one to see an error dialog)."""
        try:
            await self._async_control_heating()
        except Exception as err:
            _LOGGER.warning("Climate automatic control pass failed: %s", err)

    @callback
    def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()
        if self._is_virtual:
            self.hass.async_create_task(self._async_control_heating_safe())

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()

        if self._is_virtual:
            last_state = await self.async_get_last_state()
            if last_state is not None:
                temp_attr = last_state.attributes.get(ATTR_TEMPERATURE)
                if temp_attr is not None:
                    try:
                        self._virtual_target_temperature = float(temp_attr)
                    except (TypeError, ValueError):
                        pass
                try:
                    self._hvac_mode = HVACMode(last_state.state)
                except ValueError:
                    pass
                last_active = last_state.attributes.get("last_active_mode")
                if last_active is not None:
                    try:
                        self._last_active_mode = HVACMode(last_active)
                    except ValueError:
                        pass
            if self._virtual_target_temperature is None:
                self._virtual_target_temperature = (self._attr_min_temp + self._attr_max_temp) / 2

        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_coordinator_update)
        )
