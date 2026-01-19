"""Binary sensor platform for Tuya Heatpump."""
from __future__ import annotations
import logging
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import TuyaScaleDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Tuya Heatpump binary sensors from a config entry."""
    coordinator: TuyaScaleDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    binary_sensors = []
    
    # Online status binary sensor - HER ZAMAN EKLE
    binary_sensors.append(TuyaHeatpumpOnlineSensor(coordinator))
    _LOGGER.info("Adding online status binary sensor")
    
    # Model mapping'den binary sensörleri al
    binary_sensor_configs = coordinator.model_mapping.get("binary_sensors", {})
    
    for sensor_code, sensor_config in binary_sensor_configs.items():
        if coordinator.data and sensor_code in coordinator.data:
            binary_sensors.append(TuyaHeatpumpBinarySensor(coordinator, sensor_code, sensor_config))
            _LOGGER.info("Adding binary sensor: %s (%s)", sensor_config.get('name', sensor_code), sensor_code)
        else:
            _LOGGER.warning("Binary sensor %s not found in device data, skipping", sensor_code)
    
    async_add_entities(binary_sensors)


class TuyaHeatpumpOnlineSensor(BinarySensorEntity):
    """Representation of a Tuya Heatpump Online Status Binary Sensor."""

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
    ) -> None:
        """Initialize the online status binary sensor."""
        self.coordinator = coordinator
        
        # Device name ile unique_id oluştur
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_online_status"
        
        self._attr_name = "Online Status"
        self._attr_device_class = "connectivity"
        self._attr_has_entity_name = True
        
        # Device info
        self._attr_device_info = coordinator.device_info

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info

    @property
    def is_on(self) -> bool | None:
        """Return true if the device is online."""
        return self.coordinator.is_online

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        # Online sensörü her zaman available olmalı
        return True

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:lan-connect" if self.is_on else "mdi:lan-disconnect"

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class TuyaHeatpumpBinarySensor(BinarySensorEntity):
    """Representation of a Tuya Heatpump Binary Sensor."""

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        sensor_code: str,
        config: dict
    ) -> None:
        """Initialize the binary sensor."""
        self.coordinator = coordinator
        self._sensor_code = sensor_code
        self._config = config
        
        # Device name ile unique_id oluştur
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_{sensor_code}"
        
        self._attr_name = config.get('name', sensor_code)
        self._attr_device_class = config.get('device_class')
        self._attr_has_entity_name = True
        
        # Device info
        self._attr_device_info = coordinator.device_info

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        if not self.coordinator.data or self._sensor_code not in self.coordinator.data:
            return None
            
        raw_value = self.coordinator.data[self._sensor_code]['value']
        
        # Conversion uygula
        conversion = self._config.get('conversion', 'bool(value)')
        try:
            result = eval(conversion, {"value": raw_value, "__builtins__": {}})
            return bool(result)
        except Exception as err:
            _LOGGER.warning("Conversion failed for %s: %s", self._sensor_code, err)
            
            # Fallback conversion
            if isinstance(raw_value, bool):
                return raw_value
            elif isinstance(raw_value, (int, float)):
                return bool(raw_value)
            elif isinstance(raw_value, str):
                return raw_value.lower() in ['true', '1', 'on', 'yes', 'enable', 'open']
            
            return False

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and 
            self.coordinator.data is not None and
            self._sensor_code in self.coordinator.data
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
