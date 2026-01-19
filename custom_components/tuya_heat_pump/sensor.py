"""Sensor platform for Tuya Heatpump."""
from __future__ import annotations
import logging
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN
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
    
    # Model mapping'den sensörleri al
    sensor_configs = coordinator.model_mapping.get("sensors", {})
    
    for sensor_code, sensor_config in sensor_configs.items():
        # API'de bu code var mı kontrol et
        if coordinator.data and sensor_code in coordinator.data:
            sensors.append(TuyaHeatpumpSensor(coordinator, sensor_code, sensor_config))
            _LOGGER.info("Adding sensor: %s (%s)", sensor_config.get('name', sensor_code), sensor_code)
        elif sensor_code == "calculated_power":
            # calculated_power her zaman eklenir (API'de yok, hesaplanır)
            sensors.append(TuyaHeatpumpSensor(coordinator, sensor_code, sensor_config))
            _LOGGER.info("Adding calculated sensor: %s", sensor_config.get('name', sensor_code))
        elif sensor_code == "total_energy":
            # total_energy her zaman eklenir
            sensors.append(TuyaEnergySensor(coordinator, sensor_config))
            _LOGGER.info("Adding energy sensor: %s", sensor_config.get('name', sensor_code))
        else:
            _LOGGER.debug("Sensor %s not found in device data, skipping", sensor_code)
    
    async_add_entities(sensors)

class TuyaHeatpumpSensor(SensorEntity):
    """Representation of a Tuya Heatpump Sensor."""

    def __init__(
        self,
        coordinator: TuyaScaleDataUpdateCoordinator,
        sensor_code: str,
        config: dict
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._sensor_code = sensor_code
        self._config = config
        
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_{sensor_code}"
        
        self._attr_name = config.get('name', sensor_code)
        self._attr_native_unit_of_measurement = config.get('unit')
        self._attr_icon = config.get('icon')
        self._attr_device_class = config.get('device_class')
        self._attr_state_class = config.get('state_class')
        self._attr_has_entity_name = True
        self._attr_device_info = coordinator.device_info

    @property
    def device_info(self):
        """Return device info."""
        return self.coordinator.device_info

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self._sensor_code == "calculated_power":
            return self._calculate_power()
            
        if not self.coordinator.data or self._sensor_code not in self.coordinator.data:
            return None
            
        raw_value = self.coordinator.data[self._sensor_code]['value']
        
        # Conversion uygula
        conversion = self._config.get('conversion', 'value')
        try:
            # Güvenli eval
            result = eval(conversion, {"value": raw_value, "__builtins__": {}})
            return float(result) if isinstance(result, (int, float)) else result
        except Exception as err:
            _LOGGER.warning("Conversion failed for %s: %s", self._sensor_code, err)
            return raw_value

    def _calculate_power(self) -> float | None:
        """Güç hesaplama: P = V × I"""
        if not self.coordinator.data:
            return None
            
        voltage = None
        current = None
        
        # Model mapping'den ac_vol ve ac_curr config'lerini bul
        sensor_configs = self.coordinator.model_mapping.get("sensors", {})
        
        if 'ac_vol' in sensor_configs and 'ac_vol' in self.coordinator.data:
            config = sensor_configs['ac_vol']
            raw_voltage = self.coordinator.data['ac_vol']['value']
            conversion = config.get('conversion', 'value')
            try:
                voltage = eval(conversion, {"value": raw_voltage, "__builtins__": {}})
            except:
                voltage = raw_voltage
        
        if 'ac_curr' in sensor_configs and 'ac_curr' in self.coordinator.data:
            config = sensor_configs['ac_curr']
            raw_current = self.coordinator.data['ac_curr']['value']
            conversion = config.get('conversion', 'value')
            try:
                current = eval(conversion, {"value": raw_current, "__builtins__": {}})
            except:
                current = raw_current
        
        if voltage is not None and current is not None:
            power = voltage * current
            return round(power, 2)
            
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if self._sensor_code in ["calculated_power", "total_energy"]:
            return self.coordinator.last_update_success
            
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


class TuyaEnergySensor(SensorEntity, RestoreEntity):
    """Total Energy Sensor for Tuya Heatpump."""
    
    _attr_device_class = "energy"
    _attr_state_class = "total_increasing"
    _attr_has_entity_name = True

    def __init__(self, coordinator: TuyaScaleDataUpdateCoordinator, config: dict) -> None:
        """Initialize energy sensor."""
        self.coordinator = coordinator
        self._config = config
        self._total_energy = 0.0
        self._last_update = None
        self._last_power = 0.0
        
        device_name_slug = coordinator.device_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"{device_name_slug}_total_energy"
        self._attr_name = config.get('name', 'AC Total Energy')
        self._attr_native_unit_of_measurement = config.get('unit', 'Wh')
        self._attr_icon = config.get('icon', 'mdi:lightning-bolt')
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
        
        # Model mapping'den config'leri kullan
        sensor_configs = self.coordinator.model_mapping.get("sensors", {})
        
        if 'ac_vol' in sensor_configs and 'ac_vol' in self.coordinator.data:
            config = sensor_configs['ac_vol']
            raw_voltage = self.coordinator.data['ac_vol']['value']
            conversion = config.get('conversion', 'value')
            try:
                voltage = eval(conversion, {"value": raw_voltage, "__builtins__": {}})
                if isinstance(voltage, (int, float)) and voltage > 0:
                    voltage = float(voltage)
            except:
                voltage = None
        
        if 'ac_curr' in sensor_configs and 'ac_curr' in self.coordinator.data:
            config = sensor_configs['ac_curr']
            raw_current = self.coordinator.data['ac_curr']['value']
            conversion = config.get('conversion', 'value')
            try:
                current = eval(conversion, {"value": raw_current, "__builtins__": {}})
                if isinstance(current, (int, float)) and current > 0:
                    current = float(current)
            except:
                current = None
        
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
