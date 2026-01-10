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
    
    # Cihaz mapping'ini kontrol et
    if not coordinator.device_mapping:
        _LOGGER.error("Device mapping not found, cannot create numbers")
        async_add_entities(numbers)
        return
    
    # Mapping'e göre number'ları ekle
    number_mapping = coordinator.device_mapping.get("numbers", {})
    for number_key in NUMBER_TYPES:
        if number_key in number_mapping:
            numbers.append(TuyaHeatpumpNumber(coordinator, number_key))
            _LOGGER.info("Adding number: %s -> %s", number_key, number_mapping[number_key])
        else:
            _LOGGER.debug("Number %s not in device mapping, skipping", number_key)
    
    async_add_entities(numbers)

class TuyaHeatpumpNumber(NumberEntity):
    """Representation of a Tuya Heatpump Number."""

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        number_key: str
    ) -> None:
        """Initialize the number."""
        self.coordinator = coordinator
        self._number_key = number_key
        self._number_config = NUMBER_TYPES.get(number_key, {})
        
        # Device name ile unique_id oluştur
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_{number_key}"
        
        self._attr_name = self._number_config.get('name', number_key)
        self._attr_icon = self._number_config.get('icon')
        self._attr_native_unit_of_measurement = self._number_config.get('unit')
        self._attr_native_min_value = self._number_config.get('min_value', 0)
        self._attr_native_max_value = self._number_config.get('max_value', 100)
        self._attr_native_step = self._number_config.get('step', 1.0)
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
        if not self.coordinator.data or self._number_key not in self.coordinator.data:
            return None
            
        value_data = self.coordinator.data[self._number_key]
        value = value_data.get('value')
        
        if isinstance(value, (int, float)):
            # Yeni cihaz için değer zaten °C formatında
            # Mevcut cihaz için 10'a bölme coordinator'da yapılıyor
            return float(value)
        
        _LOGGER.warning("Unexpected value type for %s: %s", self._number_key, type(value))
        return None

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra state attributes."""
        if not self.coordinator.data or self._number_key not in self.coordinator.data:
            return {}
            
        attrs = {}
        value_data = self.coordinator.data[self._number_key]
        
        if 'last_update' in value_data:
            attrs['last_update'] = value_data['last_update']
        if 'original_dp' in value_data:
            attrs['dp_code'] = value_data['original_dp']
        
        return attrs

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        _LOGGER.info("Attempting to set %s to %s°C", self._number_key, value)
        
        success = await self.coordinator.send_command("numbers", self._number_key, value)
        
        if success:
            _LOGGER.info("✅ Successfully set %s to %s°C", self._number_key, value)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.warning("❌ Failed to set %s to %s°C", self._number_key, value)
            raise HomeAssistantError(
                f"{self._number_config.get('name', self._number_key)} değeri değiştirilemiyor. "
                f"Cihazınız bu ayarı değiştirmeye izin vermiyor. "
                f"Lütfen ayarı cihaz üzerinden yapın."
            )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and 
            self.coordinator.data is not None and
            self._number_key in self.coordinator.data
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
