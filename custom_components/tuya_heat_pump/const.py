"""Constants for the Tuya Heat Pump integration."""
from datetime import timedelta
from homeassistant.const import (
    Platform,
    UnitOfMass,
)

DOMAIN = "tuya_heat_pump"
PLATFORMS = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
    Platform.NUMBER,
    Platform.SELECT,  # Yeni ekledik
]

DEFAULT_SCAN_INTERVAL = 3
CONF_SCAN_INTERVAL = "scan_interval"

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
DEVICE_COMMAND_PATH = "/v1.0/devices/{device_id}/commands"

# Device Info
DEFAULT_NAME = "Tuya Heat Pump"
DEFAULT_MANUFACTURER = "Tuya"
DEFAULT_MODEL = "Heat Pump"

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
        "state_class": "measurement",
    },
    "out_water_temp": {
        "key": "out_water_temp",
        "name": "Out Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "tank_temp": {
        "key": "tank_temp",
        "name": "Tank Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "amb_temp": {
        "key": "amb_temp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "disc_temp": {
        "key": "disc_temp",
        "name": "Disc Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "back_temp": {
        "key": "back_temp",
        "name": "Back Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "flow_rate": {
        "key": "flow_rate",
        "name": "Water Flow Rate",
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
    "calculated_power": {
        "key": "calculated_power",
        "name": "AC Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
    },
    "total_energy": {
        "key": "total_energy", 
        "name": "AC Total Energy",
        "unit": "Wh",
        "icon": "mdi:chart-line",
        "device_class": "energy",
        "state_class": "total_increasing",
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

# Switch Types
SWITCH_TYPES = {
    "switch": {
        "key": "switch",
        "name": "Power",
        "icon": "mdi:power",
    },
    "mute": {
        "key": "mute", 
        "name": "Mute",
        "icon": "mdi:volume-off",
    },
    "holiday_sw": {
        "key": "holiday_sw",
        "name": "Holiday Mode", 
        "icon": "mdi:beach",
    },
}

# Number Types
NUMBER_TYPES = {
    "cool_temp_set": {
        "key": "cool_temp_set",
        "name": "Cool Temperature Set",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 7.0,   # 70 / 10
        "max_value": 25.0,  # 250 / 10
        "step": 1.0,
    },
    "heat_temp_set": {
        "key": "heat_temp_set", 
        "name": "Heat Temperature Set",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 25.0,  # 250 / 10
        "max_value": 65.0,  # 650 / 10
        "step": 1.0,
    },
    "hot_water_temp_set": {
        "key": "hot_water_temp_set",
        "name": "Hot Water Temperature Set", 
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 25.0,  # 250 / 10
        "max_value": 60.0,  # 600 / 10
        "step": 1.0,
    },
    "auto_temp_set": {
        "key": "auto_temp_set",
        "name": "Auto Temperature Set",
        "icon": "mdi:thermometer-auto",
        "unit": "°C", 
        "min_value": 7.0,   # 70 / 10
        "max_value": 60.0,  # 600 / 10
        "step": 1.0,
    },
}
