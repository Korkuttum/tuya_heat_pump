"""Model mapping for Tuya Heat Pump (xfmh08s3)"""

MODEL_NAME = "xfmh08s3"
# ====================================================
# Inventor Xforce @DrRikons
# ====================================================
SENSOR_TYPES = {
    "in_water_temp": {
        "dp_id": 106,
        "code": "in_water_temp",
        "name": "In Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "out_water_temp": {
        "dp_id": 107,
        "code": "out_water_temp",
        "name": "Out Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "tank_temp": {
        "dp_id": 108,
        "code": "tank_temp",
        "name": "Tank Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "amb_temp": {
        "dp_id": 118,
        "code": "amb_temp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "disc_temp": {
        "dp_id": 119,
        "code": "disc_temp",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "back_temp": {
        "dp_id": 120,
        "code": "back_temp",
        "name": "Back Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "comp_freq": {
        "dp_id": 121,
        "code": "comp_freq",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:cosine-wave",
        "state_class": "measurement",
    },
    "m_eev": {
        "dp_id": 122,
        "code": "m_eev",
        "name": "Main EEV",
        "unit": "step",
        "icon": "mdi:valve",
        "state_class": "measurement",
    },
    "a_eev": {
        "dp_id": 123,
        "code": "a_eev",
        "name": "Auxiliary EEV",
        "unit": "step",
        "icon": "mdi:valve",
        "state_class": "measurement",
    },
    "dc_fan1": {
        "dp_id": 125,
        "code": "dc_fan1",
        "name": "DC Fan 1 Speed",
        "unit": "RPM",
        "icon": "mdi:fan-speed-1",
        "state_class": "measurement",
    },
    "dc_fan2": {
        "dp_id": 126,
        "code": "dc_fan2",
        "name": "DC Fan 2 Speed",
        "unit": "RPM",
        "icon": "mdi:fan-speed-2",
        "state_class": "measurement",
    },
    "flow_rate": {
        "dp_id": 127,
        "code": "flow_rate",
        "name": "Flow Rate",
        "unit": "m³/h",
        "icon": "mdi:gauge",
        "device_class": "volume_flow_rate",
        "state_class": "measurement",        
        "conversion": "value / 10"
    },
    "ac_vol": {
        "dp_id": 128,
        "code": "ac_vol",
        "name": "AC Voltage",
        "unit": "V",
        "device_class": "voltage",
        "state_class": "measurement"
    },
    "ac_curr": {
        "dp_id": 129,
        "code": "ac_curr",
        "name": "AC Current",
        "unit": "A",
        "device_class": "current",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "calculated_power": {
        "code": "calculated_power",
        "name": "AC Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
    },
    "total_energy": {
        "code": "total_energy", 
        "name": "AC Total Energy",
        "unit": "Wh",
        "icon": "mdi:chart-line",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "tidr": {
        "dp_id": 181,
        "code": "tidr",
        "name": "Indoor Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "fault": {
        "dp_id": 6,
        "code": "fault",
        "name": "Fault",
        "icon": "mdi:alert-circle-outline",
    },
}

BINARY_SENSOR_TYPES = {
    "protect_flag": {
        "dp_id": 110,
        "code": "protect_flag",
        "name": "Protection",
        "device_class": "safety",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "freeze": {
        "dp_id": 114,
        "code": "freeze",
        "name": "Freeze Protection",
        "device_class": "cold",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "defrost": {
        "dp_id": 115,
        "code": "defrost",
        "name": "Defrost",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "pump_sta": {
        "dp_id": 116,
        "code": "pump_sta",
        "name": "Pump",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "valve": {
        "dp_id": 117,
        "code": "valve",
        "name": "4-Way Valve",
        "device_class": "opening",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "fault_flag": {
        "dp_id": 130,
        "code": "fault_flag",
        "name": "Fault Flag",
        "device_class": "problem",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "mute": {
        "dp_id": 101,
        "code": "mute",
        "name": "Mute",
        "icon": "mdi:volume-off",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "holiday_sw": {
        "dp_id": 165,
        "code": "holiday_sw",
        "name": "Holiday Mode",
        "icon": "mdi:beach",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

NUMBER_TYPES = {
    "cool_temp_set_z1": {
        "dp_id": 102,
        "code": "cool_temp_set_z1",
        "name": "Zone 1 Cool Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-minus",
        "min_value": 7.0,
        "max_value": 25.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "heat_temp_set_z1": {
        "dp_id": 103,
        "code": "heat_temp_set_z1",
        "name": "Zone 1 Heat Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-plus",
        "min_value": 30.0,
        "max_value": 65.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "hot_water_temp_set": {
        "dp_id": 104,
        "code": "hot_water_temp_set",
        "name": "Hot Water Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "min_value": 25.0,
        "max_value": 60.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "auto_cool_temp_set_z1": {
        "dp_id": 105,
        "code": "auto_cool_temp_set_z1",
        "name": "Zone 1 Auto Cool Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-auto",
        "min_value": 7.0,
        "max_value": 25.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "auto_heat_temp_set_z1": {
        "dp_id": 158,
        "code": "auto_heat_temp_set_z1",
        "name": "Zone 1 Auto Heat Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-auto",
        "min_value": 35.0,
        "max_value": 65.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "cool_temp_set_z2": {
        "dp_id": 160,
        "code": "cool_temp_set_z2",
        "name": "Zone 2 Cool Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-minus",
        "min_value": 7.0,
        "max_value": 25.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "heat_temp_set_z2": {
        "dp_id": 161,
        "code": "heat_temp_set_z2",
        "name": "Zone 2 Heat Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-plus",
        "min_value": 35.0,
        "max_value": 65.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "auto_cool_temp_set_z2": {
        "dp_id": 162,
        "code": "auto_cool_temp_set_z2",
        "name": "Zone 2 Auto Cool Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-auto",
        "min_value": 7.0,
        "max_value": 25.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "auto_heat_temp_set_z2": {
        "dp_id": 163,
        "code": "auto_heat_temp_set_z2",
        "name": "Zone 2 Auto Heat Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-auto",
        "min_value": 35.0,
        "max_value": 65.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "idr_temp_set": {
        "dp_id": 164,
        "code": "idr_temp_set",
        "name": "Indoor Room Temperature Set",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "min_value": 17.0,
        "max_value": 30.0,
        "step": 0.5,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
}

SELECT_TYPES = {
    "work_mode": {
        "dp_id": 109,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:air-conditioner",
        "options": {
            "cool": "Cool",
            "heat": "Heat",
            "auto": "Auto",
            "hot_water": "Hot Water",
            "cool_hot_water": "Cool & Hot Water",
            "heat_hot_water": "Heat & Hot Water"
        },
    },
    "zone_select": {
        "dp_id": 159,
        "code": "zone_select",
        "name": "Zone Select",
        "icon": "mdi:select",
        "options": {
            "off": "Off",
            "szone1": "Zone 1",
            "szone2": "Zone 2",
            "dzone": "Dual Zone"
        },
    },
}
