"""Number platform for Tuya Heatpump."""
from __future__ import annotations
import logging
from typing import Any

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .conversion import Conversion
from .coordinator import TuyaScaleDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Tuya Heatpump numbers from a config entry."""
    coordinator: TuyaScaleDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    numbers = []
    
    number_configs = coordinator.model_mapping.get("numbers", {})
    
    for number_code, number_config in number_configs.items():
        numbers.append(
            TuyaHeatpumpNumber(coordinator, number_code, number_config)
        )
        _LOGGER.info(
            "Adding number: %s (%s)",
            number_config.get('name', number_code),
            number_code
        )
    
    async_add_entities(numbers)


class TuyaHeatpumpNumber(NumberEntity):
    """Representation of a Tuya Heatpump Number."""

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        number_code: str,
        config: dict
    ) -> None:
        """Initialize the number."""
        self.coordinator = coordinator
        self._number_code = number_code
        self._config = config
        
        # Device name ile unique_id oluştur
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_{number_code}"
        
        self._attr_name = config.get('name', number_code)
        self._attr_icon = config.get('icon')
        self._attr_native_unit_of_measurement = config.get('unit')
        self._attr_native_min_value = config.get('min_value', 0.0)
        self._attr_native_max_value = config.get('max_value', 100.0)
        self._attr_native_step = config.get('step', 1.0)
        self._attr_has_entity_name = True
        self._attr_mode = NumberMode.BOX
        
        # Device info
        self._attr_device_info = coordinator.device_info

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        if not self.coordinator.data or self._number_code not in self.coordinator.data:
            return None
            
        raw_value = self.coordinator.data[self._number_code]['value']

        conversion = Conversion(self._config.get('conversion', 'value'))
        try:
            result = conversion.convert(raw_value)
            return float(result) if isinstance(result, (int, float)) else result
        except Exception as err:
            _LOGGER.warning("Conversion failed for %s: %s", self._number_code, err)
            return raw_value

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        _LOGGER.info("Attempting to set %s to %s %s", 
                    self._number_code, value, self._attr_native_unit_of_measurement)
        
        api_value = value
        if (api_conversion := self._config.get('api_conversion')) is not None:
            conversion = Conversion(api_conversion)
            try:
                api_value = conversion.convert(value)
                _LOGGER.debug("Converted HA value %s → API value %s", value, api_value)
            except Exception as err:
                _LOGGER.warning("API conversion failed: %s", err)
        
        success = await self.coordinator.send_command(self._number_code, api_value)
        
        if success:
            _LOGGER.info("✅ Successfully set %s to %s", self._number_code, value)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.warning("❌ Failed to set %s to %s", self._number_code, value)
            
            raise HomeAssistantError(
                f"{self._config.get('name', self._number_code)} Cannot change value of. "
                f"Your device does not allow changing this setting. "
                f"Please change the setting on the device."
            )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Tuya DP ID ve Code bilgilerini attributes'a ekle."""
        attrs: dict[str, Any] = {}

        dp_info = self.coordinator.get_tuya_dp_info(self._number_code)
        attrs["tuya_code"] = dp_info["code"]
        attrs["tuya_dp_id"] = dp_info["dp_id"]

        if self.coordinator.model_id:
            attrs["tuya_model_id"] = self.coordinator.model_id

        if self._config and isinstance(self._config, dict):
            if "values" in self._config:
                attrs["tuya_values"] = self._config["values"]

        return attrs

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and 
            self.coordinator.data is not None and
            self._number_code in self.coordinator.data
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
