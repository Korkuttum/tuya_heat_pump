"""Sensor platform for Tuya Heatpump."""
from __future__ import annotations
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .conversion import Conversion
from .coordinator import TuyaScaleDataUpdateCoordinator
from .raw_codec import decode_raw_field as _decode_raw_field
from .raw_codec import resolve_raw_source as _resolve_raw_source

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Tuya Heatpump sensors from a config entry."""
    coordinator: TuyaScaleDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    sensors = []
    
    sensor_configs = coordinator.model_mapping.get("sensors", {})
    
    for sensor_code, sensor_config in sensor_configs.items():
        # Raw-field sensor: value comes from decoding a raw payload DP
        if "field_index" in sensor_config:
            raw_source = _resolve_raw_source(coordinator, sensor_config)
            if raw_source and coordinator.data and raw_source in coordinator.data:
                # Stash the resolved source on the config so the entity
                # doesn't have to resolve it again.
                sensor_config = {**sensor_config, "raw_source": raw_source}
                sensors.append(TuyaHeatpumpSensor(coordinator, sensor_code, sensor_config))
                _LOGGER.info(
                    "Adding raw-field sensor: %s (from %s[%s])",
                    sensor_config.get('name', sensor_code),
                    raw_source,
                    sensor_config.get('field_index'),
                )
            else:
                _LOGGER.debug(
                    "Raw source for dp %s (sensor %s) not resolvable yet, skipping",
                    sensor_config.get('dp_id'), sensor_code,
                )
            continue

        if coordinator.data and sensor_code in coordinator.data:
            sensors.append(TuyaHeatpumpSensor(coordinator, sensor_code, sensor_config))
            _LOGGER.info("Adding sensor: %s (%s)", sensor_config.get('name', sensor_code), sensor_code)
        elif sensor_code == "calculated_power":
            sensors.append(TuyaHeatpumpSensor(coordinator, sensor_code, sensor_config))
            _LOGGER.info("Adding calculated sensor: %s", sensor_config.get('name', sensor_code))
        elif sensor_code == "total_energy":
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

        # Raw-field sensor: decode from the raw payload DP
        if "field_index" in self._config:
            raw_source = _resolve_raw_source(self.coordinator, self._config)
            if raw_source is None:
                return None
            if not self.coordinator.data or raw_source not in self.coordinator.data:
                return None
            b64_value = self.coordinator.data[raw_source].get('value')
            raw_value = _decode_raw_field(
                b64_value,
                self._config['field_index'],
                self._config.get('encoding', 'int32_be'),
            )
            if raw_value is None:
                return None
            # Optional conversion (scale/offset etc.)
            conversion = Conversion(self._config.get('conversion', 'value'))
            try:
                result = conversion.convert(raw_value)
                return float(result) if isinstance(result, (int, float)) else result
            except Exception as err:
                _LOGGER.warning("Conversion failed for raw %s: %s", self._sensor_code, err)
                return raw_value

        if not self.coordinator.data or self._sensor_code not in self.coordinator.data:
            return None

        raw_value = self.coordinator.data[self._sensor_code]['value']

        conversion = Conversion(self._config.get('conversion', 'value'))
        try:
            result = conversion.convert(raw_value)
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
        
        sensor_configs = self.coordinator.model_mapping.get("sensors", {})
        
        if 'ac_vol' in sensor_configs and 'ac_vol' in self.coordinator.data:
            config = sensor_configs['ac_vol']
            raw_voltage = self.coordinator.data['ac_vol']['value']
            conversion = Conversion(config.get('conversion', 'value'))
            try:
                voltage = conversion.convert(raw_voltage)
            except:
                voltage = raw_voltage
        
        if 'ac_curr' in sensor_configs and 'ac_curr' in self.coordinator.data:
            config = sensor_configs['ac_curr']
            raw_current = self.coordinator.data['ac_curr']['value']
            conversion = Conversion(config.get('conversion', 'value'))
            try:
                current = conversion.convert(raw_current)
            except:
                current = raw_current
        
        if voltage is not None and current is not None:
            power = voltage * current
            return round(power, 2)
            
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Tuya DP ID ve Code bilgilerini attributes'a ekle."""
        attrs: dict[str, Any] = {}

        if "field_index" in self._config:
            raw_source = _resolve_raw_source(self.coordinator, self._config)
            attrs["tuya_code"] = raw_source or "<unknown>"
            attrs["tuya_dp_id"] = self._config.get("dp_id")
            attrs["raw_field_index"] = self._config.get("field_index")
            attrs["raw_encoding"] = self._config.get("encoding", "int32_be")
        else:
            dp_info = self.coordinator.get_tuya_dp_info(self._sensor_code)
            attrs["tuya_code"] = dp_info["code"]
            attrs["tuya_dp_id"] = dp_info["dp_id"]

        if self.coordinator.model_id:
            attrs["tuya_model_id"] = self.coordinator.model_id

        return attrs

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if self._sensor_code in ["calculated_power", "total_energy"]:
            return self.coordinator.last_update_success

        if "field_index" in self._config:
            raw_source = _resolve_raw_source(self.coordinator, self._config)
            return (
                self.coordinator.last_update_success and
                self.coordinator.data is not None and
                raw_source is not None and
                raw_source in self.coordinator.data
            )

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
        
        if (last_state := await self.async_get_last_state()) is not None:
            try:
                self._total_energy = float(last_state.state)
                _LOGGER.info("Energy sensor state restored: %s Wh", self._total_energy)
            except (ValueError, TypeError):
                self._total_energy = 0.0
        
        self._last_power = self._get_current_power() or 0.0
        self._last_update = dt_util.utcnow()
        
        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_coordinator_update)
        )

    def _handle_coordinator_update(self) -> None:
        """Handle coordinator update."""
        current_power = self._get_current_power() or 0.0
        current_time = dt_util.utcnow()
        
        if self._last_update is not None:
            time_diff = (current_time - self._last_update).total_seconds() / 3600.0
            
            if time_diff > 0 and self._last_power > 0:
                energy_increment = self._last_power * time_diff
                self._total_energy += energy_increment
                _LOGGER.debug("Energy added: %.6f Wh, Total: %.3f Wh", energy_increment, self._total_energy)
        
        self._last_power = current_power
        self._last_update = current_time
        self.async_write_ha_state()

    def _get_current_power(self) -> float | None:
        """Get current power in watts."""
        if not self.coordinator.data:
            return None
            
        voltage = None
        current = None
        sensor_configs = self.coordinator.model_mapping.get("sensors", {})
        
        if 'ac_vol' in sensor_configs and 'ac_vol' in self.coordinator.data:
            config = sensor_configs['ac_vol']
            raw_voltage = self.coordinator.data['ac_vol']['value']
            conversion = Conversion(config.get('conversion', 'value'))
            try:
                voltage = conversion.convert(raw_voltage)
                if isinstance(voltage, (int, float)) and voltage > 0:
                    voltage = float(voltage)
            except:
                voltage = None
        
        if 'ac_curr' in sensor_configs and 'ac_curr' in self.coordinator.data:
            config = sensor_configs['ac_curr']
            raw_current = self.coordinator.data['ac_curr']['value']
            conversion = Conversion(config.get('conversion', 'value'))
            try:
                current = conversion.convert(raw_current)
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

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Tuya info for total_energy sensor."""
        attrs: dict[str, Any] = {}
        attrs["tuya_code"] = "total_energy"
        attrs["tuya_dp_id"] = None
        if self.coordinator.model_id:
            attrs["tuya_model_id"] = self.coordinator.model_id
        return attrs
