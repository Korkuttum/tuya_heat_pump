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

# Yeni
CONF_CONNECTION_TYPE = "connection_type"
CONF_IP = "ip"
CONF_LOCAL_KEY = "local_key"
CONF_PROTOCOL = "protocol"
PROTOCOL_OPTIONS = ["3.1", "3.3", "3.4", "3.5"]

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

# NOT: ESKİ SENSOR_TYPES, BINARY_SENSOR_TYPES, vs. ARTIK KULLANILMIYOR
# Bunlar artık models/default.py'de ve diğer model dosyalarında
# Bu dosyada sadece genel constant'lar ve API sabitleri kalıyor
