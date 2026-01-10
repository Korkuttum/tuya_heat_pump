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
    Platform.SELECT,
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

# DEVICE MAPPINGS - İki model için DP eşleştirmeleri
DEVICE_MAPPINGS = {
    # MODEL 1: Sizin cihazınız (000004wtcv) - Mevcut DP'ler
    "000004wtcv": {
        "name": "Standard Heat Pump",
        "sensors": {
            "in_water_temp": "in_water_temp",
            "out_water_temp": "out_water_temp",
            "tank_temp": "tank_temp",
            "amb_temp": "amb_temp",
            "disc_temp": "disc_temp",
            "back_temp": "back_temp",
            "flow_rate": "flow_rate",
            "tidr": "tidr",
            "comp_freq": "comp_freq",
            "m_eev": "m_eev",
            "a_eev": "a_eev",
            "dc_fan1": "dc_fan1",
            "dc_fan2": "dc_fan2",
            "ac_vol": "ac_vol",
            "ac_curr": "ac_curr",
            "calculated_power": "calculated_power",
            "total_energy": "total_energy",
        },
        "binary_sensors": {
            "fault": "fault",
            "protect_flag": "protect_flag",
            "freeze": "freeze",
            "defrost": "defrost",
            "pump_sta": "pump_sta",
            "valve": "valve",
            "fault_flag": "fault_flag",
        },
        "switches": {
            "switch": "switch",
            "mute": "mute",
            "holiday_sw": "holiday_sw",
        },
        "numbers": {
            "cool_temp_set": "cool_temp_set",
            "heat_temp_set": "heat_temp_set",
            "hot_water_temp_set": "hot_water_temp_set",
            "auto_temp_set": "auto_temp_set",
        },
        "selects": {
            "work_mode": "work_mode",  # Ana çalışma modu
        },
        "extra_selects": {}  # Ek select yok
    },
    
    # MODEL 2: Yeni cihaz (000004u5nz)
    "000004u5nz": {
        "name": "Advanced Heat Pump",
        "sensors": {
            "in_water_temp": "temp_top",           # Giriş suyu sıcaklığı (进水温度)
            "out_water_temp": "temp_bottom",       # Çıkış suyu sıcaklığı (出水温度)
            "tank_temp": "around_temp_f",          # Tank sıcaklığı (水箱温度)
            "amb_temp": "around_temp",             # Ortam sıcaklığı (环境温度)
            "disc_temp": "coiler_temp",            # Disk/Coil sıcaklığı (盘管温度)
            "back_temp": "effluent_temp_f",        # Geri dönüş/çıkış sıcaklığı
            "flow_rate": "venting_temp_f",         # Su akış hızı (水流量)
            "comp_freq": "compressor_strength",    # Kompresör frekansı (压缩机频率)
            "ac_vol": "voltage_current",           # AC voltaj (A相电压)
            "ac_curr": "cur_current",              # AC akım (A相电流)
            # Hesaplanan entity'ler
            "calculated_power": "__calculated__",   # cur_power'dan gelecek
            "total_energy": "electric_total",      # Toplam enerji (总电量)
        },
        "binary_sensors": {
            "fault": "fault",                      # Hata durumu (故障告警)
            "defrost": "defrost_state",            # Defrost durumu (除霜状态)
            "pump_sta": "compressor_state",        # Pompa/kompresör durumu
        },
        "switches": {
            "switch": "switch",                    # Açma/kapama (开关)
        },
        "numbers": {
            "heat_temp_set": "temp_set",           # Isıtma sıcaklık ayarı
            "hot_water_temp_set": "minitemp_set",  # Sıcak su sıcaklık ayarı
        },
        "selects": {
            "work_mode": "mode",                   # Ana çalışma modu (模式)
        },
        "extra_selects": {
            "work_profile": "work_mode",           # Çalışma profili (工作模式)
        },
        # Yeni cihazda olup standart mapte olmayan DP'ler
        "extra_sensors": {
            "power_consumption": "power_consumption",  # Günlük enerji tüketimi
            "temp_current": "temp_current",            # Ana valf (主阀)
            "venting_temp": "venting_temp",            # Egzoz sıcaklığı (排气温度)
            "effluent_temp": "effluent_temp",          # Yardımcı valf (辅阀)
            "temp_current_f": "temp_current_f",        # Yüksek basınç sat. sıcaklığı
            "top_temp_f": "top_temp_f",                # Düşük basınç sat. sıcaklığı
            "bottom_temp_f": "bottom_temp_f",          # İç coil sıcaklığı
            "effluent_temp_f": "effluent_temp_f",      # Fan frekansı
            "coiler_temp_f": "coiler_temp_f",          # Geri dönüş gaz sıcaklığı
            "eviin": "eviin",                          # Ekonomizer giriş sıcaklığı
            "eviout": "eviout",                        # Ekonomizer çıkış sıcaklığı
        }
    }
}

# Fallback model (bilinmeyen model için)
FALLBACK_MODEL = "000004wtcv"

# Tüm entity'ler için ortak tanımlar
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
        "unit": "L/min",
        "icon": "mdi:gauge",
        "device_class": None,
        "state_class": "measurement"
    },
    "tidr": {
        "key": "tidr",
        "name": "Indoor Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",   
    },
    "comp_freq": {
        "key": "comp_freq",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "device_class": None,
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
        "icon": "mdi:fan",
        "state_class": "measurement", 
    },
    "dc_fan2": {
        "key": "dc_fan2",
        "name": "DC Fan 2 Speed",
        "unit": "RPM",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    "ac_vol": {
        "key": "ac_vol",
        "name": "AC Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement", 
    },
    "ac_curr": {
        "key": "ac_curr",
        "name": "AC Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
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
        "unit": "kWh",
        "icon": "mdi:chart-line",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    # Yeni cihaz için ekstra sensörler
    "power_consumption": {
        "key": "power_consumption",
        "name": "Daily Power Consumption",
        "unit": "kWh",
        "icon": "mdi:chart-bar",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "venting_temp": {
        "key": "venting_temp",
        "name": "Exhaust Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "effluent_temp": {
        "key": "effluent_temp",
        "name": "Auxiliary Valve Position",
        "unit": "P",
        "icon": "mdi:valve",
        "state_class": "measurement",
    },
    "temp_current": {
        "key": "temp_current",
        "name": "Main Valve Position",
        "unit": "P",
        "icon": "mdi:valve",
        "state_class": "measurement",
    },
    "temp_current_f": {
        "key": "temp_current_f",
        "name": "High Pressure Saturation Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "top_temp_f": {
        "key": "top_temp_f",
        "name": "Low Pressure Saturation Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "bottom_temp_f": {
        "key": "bottom_temp_f",
        "name": "Inner Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "effluent_temp_f": {
        "key": "effluent_temp_f",
        "name": "Fan Frequency",
        "unit": "Hz",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    "coiler_temp_f": {
        "key": "coiler_temp_f",
        "name": "Return Gas Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "eviin": {
        "key": "eviin",
        "name": "Economizer Inlet Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "eviout": {
        "key": "eviout",
        "name": "Economizer Outlet Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
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

# Select Types - Ana select entity'ler
SELECT_TYPES = {
    "work_mode": {
        "key": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:air-conditioner",
        # Mevcut cihaz için options (model 000004wtcv)
        "options_model_000004wtcv": {
            "cool": "Cool",
            "heat": "Heat", 
            "auto": "Auto",
            "hot_water": "Hot Water",
            "cool_hot_water": "Cool & Hot Water",
            "heat_hot_water": "Heat & Hot Water",
            "auto_dhw": "Auto DHW"
        },
        # Yeni cihaz için options (model 000004u5nz - mode DP'si)
        "options_model_000004u5nz": {
            "cold": "Cool",
            "heating": "Heating",
            "floor_heating": "Floor Heating",
            "hot_water": "Hot Water",
            "cold_and_hotwater": "Cool & Hot Water",
            "heating_and_hot_water": "Heating & Hot Water",
            "floor_heatign_and_hot_water": "Floor Heating & Hot Water"
        }
    }
}

# Ekstra Select Types (sadece belirli modellerde)
EXTRA_SELECT_TYPES = {
    "work_profile": {
        "key": "work_profile",
        "name": "Work Profile",
        "icon": "mdi:cog",
        "options": {
            "ECO": "ECO",
            "Normal": "Normal",
            "Boost": "Boost"
        },
        "supported_models": ["000004u5nz"]  # Sadece yeni cihazda
    }
}

# Value scaling constants (DP değerlerini dönüştürmek için)
VALUE_SCALING = {
    # Model 000004wtcv için scaling (mevcut)
    "000004wtcv": {
        "temperature": 0.1,    # 10'a böl
        "current": 0.1,       # 10'a böl
        "power": 1.0,         # olduğu gibi
    },
    # Model 000004u5nz için scaling (yeni)
    "000004u5nz": {
        "temperature": 1.0,    # olduğu gibi (zaten °C)
        "current": 0.001,     # 1000'e böl (scale:3)
        "voltage": 0.1,       # 10'a böl (scale:1)
        "power": 0.1,         # 10'a böl (scale:1)
        "energy": 0.01,       # 100'e böl (scale:2)
    }
}

# Özel hesaplamalar için
CALCULATED_FIELDS = {
    "calculated_power": {
        "calculation": "voltage_current * cur_current",  # P = V * I
        "requires": ["voltage_current", "cur_current"]
    }
}
