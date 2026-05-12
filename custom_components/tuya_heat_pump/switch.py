"""Switch platform for Tuya Heatpump."""
from __future__ import annotations
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
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
    """Set up Tuya Heatpump switches from a config entry."""
    coordinator: TuyaScaleDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    switches = []
    
    # Model mapping'den switch'leri al
    switch_configs = coordinator.model_mapping.get("switches", {})
    
    for switch_code, switch_config in switch_configs.items():
        switches.append(
            TuyaHeatpumpSwitch(coordinator, switch_code, switch_config)
        )
        _LOGGER.info(
            "Adding switch: %s (%s)",
            switch_config.get('name', switch_code),
            switch_code
        )
    
    async_add_entities(switches)


class TuyaHeatpumpSwitch(SwitchEntity):
    """Representation of a Tuya Heatpump Switch."""

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        switch_code: str,
        config: dict
    ) -> None:
        """Initialize the switch."""
        self.coordinator = coordinator
        self._switch_code = switch_code
        self._config = config
        
        # Device name ile unique_id oluştur
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_{switch_code}"
        
        self._attr_name = config.get('name', switch_code)
        self._attr_icon = config.get('icon')
        self._attr_has_entity_name = True
        
        # Device info
        self._attr_device_info = coordinator.device_info

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info

    @property
    def is_on(self) -> bool | None:
        """Return true if switch is on."""
        if not self.coordinator.data or self._switch_code not in self.coordinator.data:
            return None
            
        raw_value = self.coordinator.data[self._switch_code]['value']

        conversion = Conversion(self._config.get('conversion', 'bool(value)'))
        try:
            result = conversion.convert(raw_value)
            return bool(result)
        except Exception as err:
            _LOGGER.warning("Conversion failed for %s: %s", self._switch_code, err)
            
            # Fallback conversion
            if isinstance(raw_value, bool):
                return raw_value
            elif isinstance(raw_value, (int, float)):
                return bool(raw_value)
            elif isinstance(raw_value, str):
                return raw_value.lower() in ['true', '1', 'on', 'yes', 'enable', 'open']
            
            return False

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Tuya DP ID ve Code bilgilerini attributes'a ekle."""
        attrs: dict[str, Any] = {}
        
        dp_info = self.coordinator.get_tuya_dp_info(self._switch_code)
        attrs["tuya_code"] = dp_info["code"]
        attrs["tuya_dp_id"] = dp_info["dp_id"]

        if self.coordinator.model_id:
            attrs["tuya_model_id"] = self.coordinator.model_id

        return attrs

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        _LOGGER.info("Turning ON %s", self._switch_code)

        api_value = True
        if (api_conversion := self._config.get('api_conversion')) is not None:
            conversion = Conversion(api_conversion)
            try:
                api_value = conversion.convert(api_value)
                _LOGGER.debug("Converted ON → API value %s", api_value)
            except Exception as err:
                _LOGGER.warning("API conversion failed: %s", err)
        
        success = await self.coordinator.send_command(self._switch_code, api_value)
        
        if success:
            _LOGGER.info("✅ Successfully turned ON %s", self._switch_code)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.warning("❌ Failed to turn ON %s", self._switch_code)
            raise HomeAssistantError(
                f"{self._config.get('name', self._switch_code)} cannot be turned on."
            )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        _LOGGER.info("Turning OFF %s", self._switch_code)

        api_value = False
        if (api_conversion := self._config.get('api_conversion')) is not None:
            conversion = Conversion(api_conversion)
            try:
                api_value = conversion.convert(api_value)
                _LOGGER.debug("Converted OFF → API value %s", api_value)
            except Exception as err:
                _LOGGER.warning("API conversion failed: %s", err)
        
        success = await self.coordinator.send_command(self._switch_code, api_value)
        
        if success:
            _LOGGER.info("✅ Successfully turned OFF %s", self._switch_code)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.warning("❌ Failed to turn OFF %s", self._switch_code)
            raise HomeAssistantError(
                f"{self._config.get('name', self._switch_code)} cannot be turned off."
            )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and 
            self.coordinator.data is not None and
            self._switch_code in self.coordinator.data
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
