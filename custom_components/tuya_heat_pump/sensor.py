"""Sensor platform for Tuya Heatpump."""
from __future__ import annotations
import logging
from typing import Optional

from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN, SENSOR_TYPES, DEVICE_MAPPINGS
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
    
    # Cihaz modelini kontrol et
    if not coordinator.device_mapping:
        _LOGGER.error("Device mapping not found, cannot create sensors")
        return
    
    # Ana sensörleri ekle
    sensor_mapping = coordinator.device_mapping.get("sensors", {})
    for sensor_key in SENSOR_TYPES:
        if sensor_key in sensor_mapping:
            sensors.append(TuyaHeatpumpSensor(coordinator, sensor_key))
            _LOGGER.info("Adding sensor: %s -> %s", sensor_key, sensor_mapping[sensor_key])
        else:
            _LOGGER.debug("Sensor %s not in device mapping, skipping", sensor_key)
    
    # Ekstra sensörleri ekle (yeni cihaz için)
    extra_sensors = coordinator.device_mapping.get("extra_sensors", {})
    for sensor_key, dp_code in extra_sensors.items():
        # Ekstra sensör tanımı var mı kontrol et
        if sensor_key in SENSOR_TYPES:
            sensors.append(TuyaHeatpumpSensor(coordinator, sensor_key))
            _LOGGER.info("Adding extra sensor: %s -> %s", sensor_key, dp_code)
        else:
            _LOGGER.debug("Extra sensor %s not defined in SENSOR_TYPES", sensor_key)
    
    # Total energy sensörünü ayrı ekle (her iki modelde de)
    sensors.append(TuyaEnergySensor(coordinator))
    
    async_add_entities(sensors)

class TuyaHeatpumpSensor(SensorEntity):
    """Representation of a Tuya Heatpump Sensor."""

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        sensor_key: str
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._sensor_key = sensor_key
        self._sensor_config = SENSOR_TYPES.get(sensor_key, {})
        
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_{sensor_key}"
        
        self._attr_name = self._sensor_config.get('name', sensor_key)
        self._attr_native_unit_of_measurement = self._sensor_config.get('unit')
        self._attr_icon = self._sensor_config.get('icon')
        self._attr_device_class = self._sensor_config.get('device_class')
        self._attr_state_class = self._sensor_config.get('state_class')
        self._attr_has_entity_name = True
        self._attr_device_info = coordinator.device_info

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info

    @property
    def native_value(self) -> str | float | None:
        """Return the state of the sensor."""
        if not self.coordinator.data or self._sensor_key not in self.coordinator.data:
            return None
            
        value_data = self.coordinator.data[self._sensor_key]
        value = value_data.get('value')
        
        # Debug için
        if 'original_value' in value_data:
            _LOGGER.debug("Sensor %s: %.2f (original: %s, DP: %s)", 
                         self._sensor_key, value, 
                         value_data.get('original_value'),
                         value_data.get('original_dp', 'unknown'))
        
        return value

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra state attributes."""
        if not self.coordinator.data or self._sensor_key not in self.coordinator.data:
            return {}
            
        attrs = {}
        value_data = self.coordinator.data[self._sensor_key]
        
        if 'last_update' in value_data:
            attrs['last_update'] = value_data['last_update']
        if 'original_dp' in value_data:
            attrs['dp_code'] = value_data['original_dp']
        
        return attrs

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and 
            self.coordinator.data is not None and
            self._sensor_key in self.coordinator.data
        )

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

class TuyaEnergySensor(SensorEntity, RestoreEntity):
    """Total Energy Sensor for Tuya Heatpump."""
    
    _attr_device_class = "energy"
    _attr_native_unit_of_measurement = "kWh"
    _attr_state_class = "total_increasing"
    _attr_icon = "mdi:lightning-bolt"
    _attr_has_entity_name = True

    def __init__(self, coordinator: TuyaScaleDataUpdateCoordinator) -> None:
        """Initialize energy sensor."""
        self.coordinator = coordinator
        self._total_energy = 0.0
        self._last_update = None
        self._last_power = 0.0
        
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_total_energy"
        self._attr_name = "AC Total Energy"
        self._attr_device_info = coordinator.device_info

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        
        # Restore state
        if (last_state := await self.async_get_last_state()) is not None:
            try:
                self._total_energy = float(last_state.state)
                _LOGGER.info("Energy sensor state restored: %s kWh", self._total_energy)
            except (ValueError, TypeError):
                self._total_energy = 0.0
        
        # Set initial values
        self._last_power = self._get_current_power() or 0.0
        self._last_update = dt_util.utcnow()
        
        # Listen for updates
        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_coordinator_update)
        )

    def _handle_coordinator_update(self) -> None:
        """Handle coordinator update."""
        current_power = self._get_current_power() or 0.0
        current_time = dt_util.utcnow()
        
        # Calculate energy
        if self._last_update is not None:
            time_diff = (current_time - self._last_update).total_seconds() / 3600.0  # hours
            
            if time_diff > 0 and self._last_power > 0:
                energy_increment = (self._last_power * time_diff) / 1000.0  # kWh
                self._total_energy += energy_increment
                _LOGGER.debug("Energy added: %.6f kWh, Total: %.3f kWh", 
                             energy_increment, self._total_energy)
        
        # Update values
        self._last_power = current_power
        self._last_update = current_time
        
        self.async_write_ha_state()

    def _get_current_power(self) -> Optional[float]:
        """Get current power in watts."""
        if not self.coordinator.data:
            return None
            
        # Önce calculated_power'ı kontrol et
        if "calculated_power" in self.coordinator.data:
            power_data = self.coordinator.data["calculated_power"]
            if isinstance(power_data.get('value'), (int, float)):
                return float(power_data['value'])
        
        # Sonra cur_power'ı kontrol et (yeni cihaz için)
        if "cur_power" in self.coordinator.data:
            power_data = self.coordinator.data["cur_power"]
            if isinstance(power_data.get('value'), (int, float)):
                return float(power_data['value'])
        
        return None

    @property
    def native_value(self) -> float:
        """Return the total energy in kWh."""
        return round(self._total_energy, 3)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info
