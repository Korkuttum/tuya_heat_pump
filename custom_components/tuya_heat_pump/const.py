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
    Platform.TEXT,    # Raw whole-DP string fields (username vb.)
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

# --- MQTT (tuya_sharing / Smart Life push) — tamamen opsiyonel ---
# Bunların hiçbiri mevcut kullanıcıları etkilemez: CONF_USER_CODE
# config_entry.data'da yoksa (ki mevcut tüm entry'lerde yok), MQTT hiç
# devreye girmez, entegrasyon eskisi gibi (sadece periyodik poll ile)
# çalışmaya devam eder. Sadece kurulum sırasında kullanıcı bilerek
# User Code girip QR onaylarsa aktifleşir.
CONF_USER_CODE = "user_code"
CONF_SHARING_TOKEN_INFO = "sharing_token_info"

# Herkese açık, home-assistant/core'un kendi resmi "tuya" entegrasyonunda
# kullanılan paylaşılan kimlik bilgisi (bkz. homeassistant/components/
# tuya/const.py) — Tuya'nın Home Assistant ekosistemi için ayırdığı
# ortak client_id/schema, gizli bir şey değil.
TUYA_SHARING_CLIENT_ID = "HA_3y9q4ak7g4ephrvke"
TUYA_SHARING_SCHEMA = "haauthorize"

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
DEVICE_COMMAND_PATH = "/v2.0/cloud/thing/{device_id}/shadow/properties/issue"  # ← Değişiklik: v2.0 komut gönderme endpoint'i

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
