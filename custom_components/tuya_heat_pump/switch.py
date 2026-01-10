"""Switch platform for Tuya Heatpump."""
from __future__ import annotations
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError

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
    
    # Cihaz mapping'ini kontrol et
    if not coordinator.device_mapping:
        _LOGGER.error("Device mapping not found, cannot create switches")
        async_add_entities(switches)
        return
    
    # Mapping'e göre switch'leri ekle
    switch_mapping = coordinator.device_mapping.get("switches", {})
    for switch_key in SWITCH_TYPES:
        if switch_key in switch_mapping:
            switches.append(TuyaHeatpumpSwitch(coordinator, switch_key))
            _LOGGER.info("Adding switch: %s -> %s", switch_key, switch_mapping[switch_key])
        else:
            _LOGGER.debug("Switch %s not in device mapping, skipping", switch_key)
    
    async_add_entities(switches)

class TuyaHeatpumpSwitch(SwitchEntity):
    """Representation of a Tuya Heatpump Switch."""

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        switch_key: str
    ) -> None:
        """Initialize the switch."""
        self.coordinator = coordinator
        self._switch_key = switch_key
        self._switch_config = SWITCH_TYPES.get(switch_key, {})
        
        # Device name ile unique_id oluştur
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_{switch_key}"
        
        self._attr_name = self._switch_config.get('name', switch_key)
        self._attr_icon = self._switch_config.get('icon')
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
        if not self.coordinator.data or self._switch_key not in self.coordinator.data:
            return None
            
        value_data = self.coordinator.data[self._switch_key]
        value = value_data.get('value')
        
        # Value'yu boolean'a çevir
        if isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return bool(value)
        elif isinstance(value, str):
            return value.lower() in ['true', '1', 'on', 'yes', 'enable', 'open']
        
        return False

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra state attributes."""
        if not self.coordinator.data or self._switch_key not in self.coordinator.data:
            return {}
            
        attrs = {}
        value_data = self.coordinator.data[self._switch_key]
        
        if 'last_update' in value_data:
            attrs['last_update'] = value_data['last_update']
        if 'original_dp' in value_data:
            attrs['dp_code'] = value_data['original_dp']
        
        return attrs

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        _LOGGER.info("Turning ON %s", self._switch_key)
        success = await self.coordinator.send_command("switches", self._switch_key, True)
        
        if success:
            _LOGGER.info("✅ Successfully turned ON %s", self._switch_key)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.warning("❌ Failed to turn ON %s", self._switch_key)
            raise HomeAssistantError(
                f"{self._switch_config.get('name', self._switch_key)} açılamıyor. "
                f"Cihazınız bu özelliği değiştirmeye izin vermiyor. "
                f"Lütfen ayarı cihaz üzerinden yapın."
            )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        _LOGGER.info("Turning OFF %s", self._switch_key)
        success = await self.coordinator.send_command("switches", self._switch_key, False)
        
        if success:
            _LOGGER.info("✅ Successfully turned OFF %s", self._switch_key)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.warning("❌ Failed to turn OFF %s", self._switch_key)
            raise HomeAssistantError(
                f"{self._switch_config.get('name', self._switch_key)} kapatılamıyor. "
                f"Cihazınız bu özelliği değiştirmeye izin vermiyor. "
                f"Lütfen ayarı cihaz üzerinden yapın."
            )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and 
            self.coordinator.data is not None and
            self._switch_key in self.coordinator.data
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
