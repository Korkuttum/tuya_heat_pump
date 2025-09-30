"""Support for Tuya Scale binary sensors."""
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    BINARY_SENSOR_TYPES,
    DEFAULT_NAME,
    DEFAULT_MANUFACTURER,
    DEFAULT_MODEL,
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Tuya Scale binary sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = []
    for sensor_type, sensor_info in BINARY_SENSOR_TYPES.items():
        sensors.append(
            TuyaScaleBinarySensor(
                coordinator,
                sensor_info["key"],
                sensor_info["name"],
                sensor_info.get("device_class"),
                sensor_info.get("icon"),
            )
        )

    async_add_entities(sensors)


class TuyaScaleBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Tuya Scale Binary Sensor."""

    def __init__(self, coordinator, key, name, device_class=None, icon=None):
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_device_class = device_class
        self._attr_icon = icon

        self._attr_unique_id = f"{coordinator.device_id}_{key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device_id)},
            "name": DEFAULT_NAME,
            "manufacturer": DEFAULT_MANUFACTURER,
            "model": DEFAULT_MODEL,
        }

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if self.coordinator.data is None:
            return None

        # Veri dict olarak geliyor, içindeki 'value' anahtarını kullan
        sensor_data = self.coordinator.data.get(self._key)
        if sensor_data is None:
            return False

        return bool(sensor_data.get('value', False))
