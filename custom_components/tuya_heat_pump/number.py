"""Number platform for Tuya Heatpump."""
from __future__ import annotations
import logging
from typing import Any

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, NUMBER_TYPES
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
    for number_type in NUMBER_TYPES:
        if coordinator.data and number_type in coordinator.data:
            numbers.append(TuyaHeatpumpNumber(coordinator, number_type))
            _LOGGER.info("Adding number: %s", number_type)
        else:
            _LOGGER.warning("Number %s not found in device data, skipping", number_type)
    
    async_add_entities(numbers)

class TuyaHeatpumpNumber(NumberEntity):
    """Representation of a Tuya Heatpump Number."""

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        number_type: str
    ) -> None:
        """Initialize the number."""
        self.coordinator = coordinator
        self._number_type = number_type
        
        # Device name ile unique_id oluştur
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_{number_type}"
        
        self._attr_name = NUMBER_TYPES[number_type]['name']
        self._attr_icon = NUMBER_TYPES[number_type].get('icon')
        self._attr_native_unit_of_measurement = NUMBER_TYPES[number_type]['unit']
        self._attr_native_min_value = NUMBER_TYPES[number_type]['min_value']
        self._attr_native_max_value = NUMBER_TYPES[number_type]['max_value']
        self._attr_native_step = NUMBER_TYPES[number_type]['step']
        self._attr_has_entity_name = True
        self._attr_mode = NumberMode.BOX  # Slider yerine box modu
        
        # Device info
        self._attr_device_info = coordinator.device_info

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        if not self.coordinator.data or self._number_type not in self.coordinator.data:
            return None
            
        value = self.coordinator.data[self._number_type]['value']
        
        # API'den gelen değeri °C'ye çevir (10'a böl)
        if isinstance(value, (int, float)):
            return value / 10.0
        
        _LOGGER.warning("Unexpected value type for %s: %s", self._number_type, type(value))
        return None

    async def async_set_native_value(self, value: float) -> None:
        """Set new value - try to write, show error if fails."""
        # Değeri API formatına çevir (10 ile çarp ve integer'a çevir)
        api_value = int(value * 10)
        
        _LOGGER.info("Attempting to set %s to %s°C (API value: %s)", 
                    self._number_type, value, api_value)
        
        success = await self.coordinator.send_command(self._number_type, api_value)
        
        if success:
            _LOGGER.info("✅ Successfully set %s to %s°C", self._number_type, value)
            # Başarılı ise state'i güncelle
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.warning("❌ Failed to set %s to %s°C", self._number_type, value)
            
            # Kullanıcıya Home Assistant bildirimi göster
            raise HomeAssistantError(
                f"{NUMBER_TYPES[self._number_type]['name']} değeri değiştirilemiyor. "
                f"Cihazınız bu ayarı değiştirmeye izin vermiyor. "
                f"Lütfen ayarı cihaz üzerinden yapın."
            )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and 
            self.coordinator.data is not None and
            self._number_type in self.coordinator.data
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
