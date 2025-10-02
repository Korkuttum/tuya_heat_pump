"""Constants for the Tuya Scale integration."""
from datetime import timedelta
from homeassistant.const import (
    Platform,
    UnitOfMass,
)

DOMAIN = "tuya_heatpump"
PLATFORMS = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]
# Eski SCAN_INTERVAL sabitini kaldırıp yerine aşağıdaki iki satırı ekliyoruz
DEFAULT_SCAN_INTERVAL = 10  # Varsayılan değer (dakika cinsinden)
CONF_SCAN_INTERVAL = "scan_interval"  # Yeni yapılandırma sabiti

# Configuration
CONF_ACCESS_ID = "access_id"
CONF_ACCESS_KEY = "access_key"
CONF_DEVICE_ID = "device_id"
CONF_REGION = "region"

# API Region
DEFAULT_REGION = "EU"
REGIONS = {
    "EU": "https://openapi.tuyaeu.com",
    "US": "https://openapi.tuyaus.com",
    "CN": "https://openapi.tuyacn.com",
    "IN": "https://openapi.tuyain.com"
}

# API Paths
TOKEN_PATH = "/v1.0/token?grant_type=1"
DEVICE_DATA_PATH = "/v2.0/cloud/thing/{device_id}/shadow/properties"

# Device Info
DEFAULT_NAME = "Tuya Heatpump"
DEFAULT_MANUFACTURER = "Tuya"
DEFAULT_MODEL = "Heatpump"

# Error Messages
ERROR_AUTH = "Authentication failed"
ERROR_CONN = "Failed to connect"
ERROR_TIMEOUT = "Connection timeout"

# Current values
CURRENT_USER = "Korkuttum"
CURRENT_TIME = "2025-05-29 14:10:10"

# Sensor Types
SENSOR_TYPES = {
    "in_water_temp": {
        "key": "in_water_temp",
        "name": "In Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "temperature",
    },
    "out_water_temp": {
        "key": "out_water_temp",
        "name": "Out Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "temperature",
    },
    "tank_temp": {
        "key": "tank_temp",
        "name": "Tank Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "temperature",
    },
    "amb_temp": {
        "key": "amb_temp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "temperature",
    },
    "disc_temp": {
        "key": "disc_temp",
        "name": "Disc Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "temperature",
    },
    "back_temp": {
        "key": "back_temp",
        "name": "Back Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "temperature",
    },
    "flow_rate": {
        "key": "flow_rate",
        "name": "Water Pressure",
        "unit": "m³/H",
        "icon": "mdi:gauge",
        "device_class": "pressure",
        "state_class": "measurement"
    },
    "tidr": {
        "key": "tidr",
        "name": "Indoor Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "temperature",   
    },
    "comp_freq": {
        "key": "comp_freq",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:cosine-wave",
        "device_class": "Frequency",
        "state_class": "measurement",   
    },
    "m_eev": {
        "key": "m_eev",
        "name": "Main EEV Position",
        "unit": "step",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement", 
    },
    "a_eev": {
        "key": "a_eev",
        "name": "Auxiliary EEV Position",
        "unit": "step",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",  
    },
    "dc_fan1": {
        "key": "dc_fan1",
        "name": "DC Fan 1 Speed",
        "unit": "RPM",
        "icon": "mdi:fan-speed-1",
        "state_class": "measurement", 
    },
    "dc_fan2": {
        "key": "dc_fan2",
        "name": "DC Fan 2 Speed",
        "unit": "RPM",
        "icon": "mdi:fan-speed-2",
        "state_class": "measurement",
    },
    "ac_vol": {
        "key": "ac_vol",
        "name": "AC Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "Voltage",
        "state_class": "measurement", 
    },
    "ac_curr": {
        "key": "ac_curr",
        "name": "AC Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "Current",
        "state_class": "measurement", 
    },
}

# Binary Sensor Types
BINARY_SENSOR_TYPES = {
    "fault": {
        "key": "fault",
        "name": "Fault Status",
        "device_class": "problem",
    },
    "protect_flag": {
        "key": "protect_flag",
        "name": "Protection Status",
        "device_class": "safety",
    },
    "freeze": {
        "key": "freeze",
        "name": "Freeze Status",
        "device_class": "cold",
    },
    "defrost": {
        "key": "defrost",
        "name": "Defrost Status",
        "device_class": "heat",
    },
    "pump_sta": {
        "key": "pump_sta",
        "name": "Pump Status",
        "device_class": "running",
    },
    "valve": {
        "key": "valve",
        "name": "Valve Status",
        "device_class": "opening",
    },
    "fault_flag": {
        "key": "fault_flag",
        "name": "Fault Flag",
        "device_class": "problem",
    },
}
