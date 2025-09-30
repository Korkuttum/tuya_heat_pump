"""Support for Tuya Scale sensors."""
import logging
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfMass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SENSOR_TYPES,
    DEFAULT_NAME,
    DEFAULT_MANUFACTURER,
    DEFAULT_MODEL,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Tuya Scale sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    sensors = []
    
    for sensor_type, sensor_info in SENSOR_TYPES.items():
        key = sensor_info["key"]
        if coordinator.data is not None and key in coordinator.data:
            sensors.append(TuyaScaleSensor(
                coordinator,
                key,
                sensor_info["name"],
                sensor_info.get("unit"),
                sensor_info.get("icon"),
                sensor_info.get("device_class"),
                sensor_info.get("state_class")
            ))
    
    async_add_entities(sensors)

class TuyaScaleSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Tuya Scale Sensor."""

    def __init__(self, coordinator, key, name, unit=None, icon=None, device_class=None, state_class=None):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        self._attr_name = f"{DEFAULT_NAME} {name}"
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_unique_id = f"{coordinator.device_id}_{key}"
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device_id)},
            "name": DEFAULT_NAME,
            "manufacturer": DEFAULT_MANUFACTURER,
            "model": DEFAULT_MODEL,
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None or self._key not in self.coordinator.data:
            return None

        data = self.coordinator.data[self._key]
        if isinstance(data, dict):
            value = data.get('value')
        else:
            value = data

        if value is None:
            return None

        # Tüm sensör değerlerini 10'a böl
        try:
            return float(value) / 10
        except (ValueError, TypeError):
            return value

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self.coordinator.data is None or self._key not in self.coordinator.data:
            return None

        data = self.coordinator.data[self._key]
        if not isinstance(data, dict):
            return None

        return {
            "last_update": data.get("last_update"),
            "timestamp": data.get("timestamp"),
            "raw_value": data.get("value")
        }
