"""Sensor platform for Tuya Heatpump."""
from __future__ import annotations
import logging
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import dt as dt_util

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
    
    # Normal sensörleri ekle
    for sensor_type in SENSOR_TYPES:
        if sensor_type == 'total_energy':
            continue  # Bunu ayrı ekleyeceğiz
        elif sensor_type in ['calculated_power']:
            sensors.append(TuyaHeatpumpSensor(coordinator, sensor_type))
            _LOGGER.info("Adding calculated sensor: %s", sensor_type)
        elif coordinator.data and sensor_type in coordinator.data:
            sensors.append(TuyaHeatpumpSensor(coordinator, sensor_type))
            _LOGGER.info("Adding sensor: %s", sensor_type)
        else:
            _LOGGER.debug("Sensor %s not found in device data, skipping", sensor_type)
    
    # Total energy sensörünü ayrı ekle
    sensors.append(TuyaEnergySensor(coordinator))
    
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
        
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_{sensor_type}"
        
        self._attr_name = SENSOR_TYPES[sensor_type]['name']
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]['unit']
        self._attr_icon = SENSOR_TYPES[sensor_type].get('icon')
        self._attr_device_class = SENSOR_TYPES[sensor_type].get('device_class')
        self._attr_state_class = SENSOR_TYPES[sensor_type].get('state_class')
        self._attr_has_entity_name = True
        self._attr_device_info = coordinator.device_info

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self._sensor_type == "calculated_power":
            return self._calculate_power()
            
        if not self.coordinator.data or self._sensor_type not in self.coordinator.data:
            return None
            
        value = self.coordinator.data[self._sensor_type]['value']
        
        if self._sensor_type in ['in_water_temp', 'out_water_temp', 'tank_temp', 'amb_temp', 
                                'disc_temp', 'back_temp', 'tidr', 'ac_curr', 'flow_rate']:
            if isinstance(value, (int, float)):
                return value / 10.0
        
        return value

    def _calculate_power(self) -> float | None:
        """Güç hesaplama: P = V × I"""
        if not self.coordinator.data:
            return None
            
        voltage = None
        current = None
        
        if 'ac_vol' in self.coordinator.data:
            voltage = self.coordinator.data['ac_vol']['value']
            if isinstance(voltage, (int, float)):
                voltage = voltage
        
        if 'ac_curr' in self.coordinator.data:
            current = self.coordinator.data['ac_curr']['value']
            if isinstance(current, (int, float)):
                current = current / 10.0
        
        if voltage is not None and current is not None:
            power = voltage * current
            return round(power, 2)
            
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if self._sensor_type in ['calculated_power']:
            return self.coordinator.last_update_success
            
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


class TuyaEnergySensor(SensorEntity, RestoreEntity):
    """Total Energy Sensor for Tuya Heatpump."""
    
    _attr_device_class = "energy"
    _attr_native_unit_of_measurement = "Wh"
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
                _LOGGER.info("Energy sensor state restored: %s Wh", self._total_energy)
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
                energy_increment = self._last_power * time_diff  # Wh
                self._total_energy += energy_increment
                _LOGGER.debug("Energy added: %.6f Wh, Total: %.3f Wh", energy_increment, self._total_energy)
        
        # Update values
        self._last_power = current_power
        self._last_update = current_time
        
        self.async_write_ha_state()

    def _get_current_power(self) -> float | None:
        """Get current power in watts."""
        if not self.coordinator.data:
            return None
            
        voltage = None
        current = None
        
        if 'ac_vol' in self.coordinator.data:
            voltage = self.coordinator.data['ac_vol']['value']
            if isinstance(voltage, (int, float)) and voltage > 0:
                voltage = float(voltage)
        
        if 'ac_curr' in self.coordinator.data:
            current = self.coordinator.data['ac_curr']['value']
            if isinstance(current, (int, float)) and current > 0:
                current = float(current) / 10.0
        
        if voltage is not None and current is not None:
            return voltage * current
        
        return None

    @property
    def native_value(self) -> float:
        """Return the total energy in Wh."""
        return round(self._total_energy, 3)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info
