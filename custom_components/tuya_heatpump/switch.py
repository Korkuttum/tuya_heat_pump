"""Switch platform for Tuya Heatpump."""
from __future__ import annotations
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, SWITCH_TYPES
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
    for switch_type in SWITCH_TYPES:
        # Sadece verilerde mevcut olan switch'leri ekle
        if coordinator.data and switch_type in coordinator.data:
            switches.append(TuyaHeatpumpSwitch(coordinator, switch_type))
            _LOGGER.info("Adding switch: %s", switch_type)
        else:
            _LOGGER.warning("Switch %s not found in device data, skipping", switch_type)
    
    async_add_entities(switches)

class TuyaHeatpumpSwitch(SwitchEntity):
    """Representation of a Tuya Heatpump Switch."""

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        switch_type: str
    ) -> None:
        """Initialize the switch."""
        self.coordinator = coordinator
        self._switch_type = switch_type
        
        self._attr_unique_id = f"{coordinator.device_id}_{switch_type}"
        self._attr_name = SWITCH_TYPES[switch_type]['name']
        self._attr_icon = SWITCH_TYPES[switch_type].get('icon')
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
        if not self.coordinator.data or self._switch_type not in self.coordinator.data:
            return None
            
        value = self.coordinator.data[self._switch_type]['value']
        
        # Value'yu boolean'a çevir
        if isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return bool(value)
        elif isinstance(value, str):
            return value.lower() in ['true', '1', 'on', 'yes', 'enable', 'open']
        
        return False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        _LOGGER.info("Turning ON %s", self._switch_type)
        success = await self.coordinator.send_command(self._switch_type, True)
        if not success:
            _LOGGER.error("Failed to turn on %s", self._switch_type)
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        _LOGGER.info("Turning OFF %s", self._switch_type)
        success = await self.coordinator.send_command(self._switch_type, False)
        if not success:
            _LOGGER.error("Failed to turn off %s", self._switch_type)
            self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and 
            self.coordinator.data is not None and
            self._switch_type in self.coordinator.data
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )