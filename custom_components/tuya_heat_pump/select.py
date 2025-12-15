"""Select platform for Tuya Heatpump."""
from __future__ import annotations
import logging
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, SELECT_TYPES
from .coordinator import TuyaScaleDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Tuya Heatpump selects from a config entry."""
    coordinator: TuyaScaleDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    selects = []
    for select_type in SELECT_TYPES:
        if coordinator.data and select_type in coordinator.data:
            selects.append(TuyaHeatpumpSelect(coordinator, select_type))
            _LOGGER.info("Adding select: %s", select_type)
        else:
            _LOGGER.warning("Select %s not found in device data, skipping", select_type)
    
    async_add_entities(selects)

class TuyaHeatpumpSelect(SelectEntity):
    """Representation of a Tuya Heatpump Select."""

    _attr_translation_key = "work_mode"  # BU ÇOK ÖNEMLİ!
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        select_type: str
    ) -> None:
        """Initialize the select."""
        self.coordinator = coordinator
        self._select_type = select_type
        
        # Device name ile unique_id oluştur
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_{select_type}"
        
        # Translation key zaten ayarlandı, name gerek yok
        self._attr_icon = SELECT_TYPES[select_type].get('icon')
        
        # Options'ları API'den gelen değerler olarak bırak
        self._attr_options = list(SELECT_TYPES[select_type]['options'].keys())
        
        # Device info
        self._attr_device_info = coordinator.device_info

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        if not self.coordinator.data or self._select_type not in self.coordinator.data:
            return None
            
        value = self.coordinator.data[self._select_type]['value']
        if isinstance(value, str):
            return value
        
        _LOGGER.warning("Unexpected value type for %s: %s", self._select_type, type(value))
        return None

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.info("Changing %s to %s", self._select_type, option)
        
        success = await self.coordinator.send_command(self._select_type, option)
        
        if success:
            _LOGGER.info("✅ Successfully changed %s to %s", self._select_type, option)
            # Başarılı ise state'i güncelle
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.warning("❌ Failed to change %s to %s", self._select_type, option)
            
            # Kullanıcıya Home Assistant bildirimi göster
            raise HomeAssistantError(
                f"Work mode değiştirilemiyor. "
                f"Cihazınız bu modu değiştirmeye izin vermiyor. "
                f"Lütfen modu cihaz üzerinden yapın."
            )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and 
            self.coordinator.data is not None and
            self._select_type in self.coordinator.data
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )