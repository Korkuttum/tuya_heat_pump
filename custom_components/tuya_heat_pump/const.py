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
    Platform.CLIMATE,  # Opsiyonel, varsayılan kapalı — bkz. climate.py
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

# Cloud API access_token cache'i (bkz. issue #77). Coordinator her
# async_setup_entry retry'sinde SIFIRDAN oluşturuluyor, bu yüzden
# _get_token()'ın in-memory cache'i (self.access_token) retry'lar arası
# hayatta kalmıyor — her retry, hâlâ geçerli bir token varken bile onu
# yeniden almak için ~10-20sn'lik bir network round-trip'i baştan
# yapıyordu. Bu iki alan token'ı entry.data'ya yazarak retry'lar arası
# (ve HA restart'ları arası) hayatta kalmasını sağlıyor.
CONF_CACHED_ACCESS_TOKEN = "cached_access_token"
CONF_CACHED_TOKEN_EXPIRES_AT = "cached_token_expires_at"

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

# --- Opsiyonel climate (termostat) entity'si ---
# Kesinlikle kullanıcı tercihi: varsayılan kapalı (CONF_CLIMATE_ENABLED
# yoksa/False ise climate.py hiçbir entity oluşturmaz). Birçok model bir
# havuz ısı pompası (kontrol edilen değer su sıcaklığı, oda değil) ve
# bazı modellerde Tuya'nın kendi app'i zaten dahili bir oda termostatı
# döngüsü çalıştırıyor olabilir — bu yüzden HA tarafında ikinci bir
# kontrol döngüsü ancak kullanıcı açıkça isterse oluşturulmalı. Power/
# current/target/mode-select hepsi model_mapping'teki DÜZ (raw olmayan)
# birer dict key — switch.py/number.py/sensor.py/select.py'nin zaten
# okuduğu aynı DP'ler, ayrı bir veri yolu değil.
#
# İki alt mod var (climate.py karar veriyor, kullanıcı seçmiyor):
# - "Direct": cihazın kendi yazılabilir hedef sıcaklığı (CLIMATE_TARGET_
#   TEMP_CODE) seçiliyse, climate kartı doğrudan o DP'ye yazar — cihaz
#   zaten kendi kapalı döngüsünü çalıştırıyor, biz sadece arayüzüyüz.
# - "Virtual": hedef seçilmediyse ama current seçiliyse, climate kartı
#   HA'nın kendi generic_thermostat'ı gibi davranır — hedefi kendi
#   içinde tutar (cihaza hiç yazmaz) ve Power switch'i current/target
#   karşılaştırmasıyla (tolerans + min. çevrim süresi korumalı) kendisi
#   açıp kapatır.
CONF_CLIMATE_ENABLED = "climate_enabled"
CONF_CLIMATE_POWER_CODE = "climate_power_code"
CONF_CLIMATE_CURRENT_TEMP_CODE = "climate_current_temp_code"
CONF_CLIMATE_TARGET_TEMP_CODE = "climate_target_temp_code"

# Soğutma modu — opsiyonel. Model dosyasındaki bir SELECT_TYPES entity'si
# (örn. "work_mode") ısı/soğutma modunu seçiyorsa, o select'in hangi ham
# değerinin heat/cool anlamına geldiğini burada tutuyoruz. İkisi de
# seçilmemişse climate kartı sadece HEAT/OFF sunar (mevcut davranış).
CONF_CLIMATE_MODE_SELECT_CODE = "climate_mode_select_code"
CONF_CLIMATE_HEAT_VALUE = "climate_heat_value"
CONF_CLIMATE_COOL_VALUE = "climate_cool_value"

# Tolerans ve min. çevrim süresi sadece "virtual" modda kullanılır (bkz.
# yukarı). Min/maks hedef sıcaklık ise HER İKİ modda da kullanılır — bazı
# model dosyalarında cihazın kendi target DP'si için sadece genel/
# placeholder bir aralık (örn. 0-100) tanımlı olabiliyor, bu yüzden
# kullanıcı burada her zaman geçersiz kılabilsin diye direct modda da
# zorunlu kılınmıyor (Options formunda sadece cihazın kendi değeri bir
# ÖNERİ olarak önceden dolduruluyor — bkz. config_flow.py).
CONF_CLIMATE_TOLERANCE = "climate_tolerance"
CONF_CLIMATE_MIN_CYCLE_MINUTES = "climate_min_cycle_minutes"
CONF_CLIMATE_MIN_TEMP = "climate_min_temp"
CONF_CLIMATE_MAX_TEMP = "climate_max_temp"

DEFAULT_CLIMATE_TOLERANCE = 0.3
DEFAULT_CLIMATE_MIN_CYCLE_MINUTES = 5
DEFAULT_CLIMATE_MIN_TEMP = 5
DEFAULT_CLIMATE_MAX_TEMP = 30
