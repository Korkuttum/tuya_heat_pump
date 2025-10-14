"""Sensor platform for Tuya Heatpump."""
from __future__ import annotations
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, SENSOR_TYPES
from .coordinator import TuyaScaleDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Tuya Heatpump sensors from a config entry."""
    coordinator: TuyaScaleDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    sensors = []
    for sensor_type in SENSOR_TYPES:
        if coordinator.data and sensor_type in coordinator.data:
            sensors.append(TuyaHeatpumpSensor(coordinator, sensor_type))
            _LOGGER.info("Adding sensor: %s", sensor_type)
        else:
            _LOGGER.warning("Sensor %s not found in device data, skipping", sensor_type)
    
    async_add_entities(sensors)

class TuyaHeatpumpSensor(SensorEntity):
    """Representation of a Tuya Heatpump Sensor."""

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        sensor_type: str
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._sensor_type = sensor_type
        
        # Device name ile unique_id oluştur
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_{sensor_type}"
        
        self._attr_name = SENSOR_TYPES[sensor_type]['name']
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]['unit']
        self._attr_icon = SENSOR_TYPES[sensor_type].get('icon')
        self._attr_device_class = SENSOR_TYPES[sensor_type].get('device_class')
        self._attr_state_class = SENSOR_TYPES[sensor_type].get('state_class')
        self._attr_has_entity_name = True
        
        # Device info
        self._attr_device_info = coordinator.device_info

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if not self.coordinator.data or self._sensor_type not in self.coordinator.data:
            return None
            
        value = self.coordinator.data[self._sensor_type]['value']
        
        # Temperature değerlerini 10'a böl
        if self._sensor_type in ['in_water_temp', 'out_water_temp', 'tank_temp', 'amb_temp', 
                                'disc_temp', 'back_temp', 'tidr', 'ac_curr', 'flow_rate']:
            if isinstance(value, (int, float)):
                return value / 10.0
        
        return value

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and 
            self.coordinator.data is not None and
            self._sensor_type in self.coordinator.data
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
