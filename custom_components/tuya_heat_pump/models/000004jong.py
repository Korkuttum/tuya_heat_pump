"""Model mapping for EV DC R290 Heat Pump (000004jong)."""

MODEL_NAME = "Power World PW030 Heat Pump (000004jong)"
# ====================================================
# Power World PW030 @HeideggerDaniel
# ====================================================
SENSOR_TYPES = {
    # Inlet Water Temperature (dp_id: 101)
    "intemp": {
        "dp_id": 101,
        "code": "intemp",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Outlet Water Temperature (dp_id: 102)
    "outtemp": {
        "dp_id": 102,
        "code": "outtemp",
        "name": "Outlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Ambient Temperature (dp_id: 103)
    "whjtemp": {
        "dp_id": 103,
        "code": "whjtemp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Exhaust / Discharge Temperature (dp_id: 104)
    "cmptemp": {
        "dp_id": 104,
        "code": "cmptemp",
        "name": "Exhaust Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Suction / Return Gas Temperature (dp_id: 105)
    "hqtemp": {
        "dp_id": 105,
        "code": "hqtemp",
        "name": "Suction Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Outdoor Coil Temperature (dp_id: 106)
    "ptemp": {
        "dp_id": 106,
        "code": "ptemp",
        "name": "Outdoor Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Cooling Coil Temperature (dp_id: 107)
    "cptemp": {
        "dp_id": 107,
        "code": "cptemp",
        "name": "Cooling Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Tank / Water Tank Temperature (dp_id: 108)
    "wttemp": {
        "dp_id": 108,
        "code": "wttemp",
        "name": "Water Tank Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Main Expansion Valve Opening (dp_id: 109)
    "step_run": {
        "dp_id": 109,
        "code": "step_run",
        "name": "Main Expansion Valve Opening",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    # Enthalpy Expansion Valve Opening (dp_id: 111)
    "stepb_run": {
        "dp_id": 111,
        "code": "stepb_run",
        "name": "Enthalpy Expansion Valve Opening",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    # Compressor Current (dp_id: 112)
    "cmp_cur": {
        "dp_id": 112,
        "code": "cmp_cur",
        "name": "Compressor Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
    },
    # Heatsink Temperature (dp_id: 113)
    "sink_temp": {
        "dp_id": 113,
        "code": "sink_temp",
        "name": "Heatsink Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # DC Bus Voltage (dp_id: 114)
    "dc_bus_voltage": {
        "dp_id": 114,
        "code": "dc_bus_voltage",
        "name": "DC Bus Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    # Compressor Actual Frequency (dp_id: 115)
    "cmp_act_frep": {
        "dp_id": 115,
        "code": "cmp_act_frep",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "state_class": "measurement",
    },
    # DC Fan 1 Speed (dp_id: 116)
    "dc_fan_speed": {
        "dp_id": 116,
        "code": "dc_fan_speed",
        "name": "DC Fan 1 Speed",
        "unit": "RPM",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    # DC Fan 2 Speed (dp_id: 117)
    "dc_fan2_speed": {
        "dp_id": 117,
        "code": "dc_fan2_speed",
        "name": "DC Fan 2 Speed",
        "unit": "RPM",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    # Fault Code - Raw Bitmap Value (dp_id: 15)
    "fault_code": {
        "dp_id": 15,
        "code": "fault_code",
        "name": "Fault Code",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    # Fault Status (dp_id: 15)
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
}

# ====================================================
# SWITCH TYPES (read-write bool - accessMode: "rw")
# ====================================================
SWITCH_TYPES = {
    # Power Switch (dp_id: 1)
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Reset to Default (dp_id: 125) - accessMode: "wr"
    "reset": {
        "dp_id": 125,
        "code": "reset",
        "name": "Reset to Default",
        "icon": "mdi:restore",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    # Operation Mode (dp_id: 2) - smart, strong, mute
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Operation Mode",
        "icon": "mdi:hvac",
        "options": {
            "smart": "Smart",
            "strong": "Strong",
            "mute": "Mute",
        },
    },
    # Work Mode (dp_id: 5) - wth, heat, cool, wth_heat, wth_cool
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:cog",
        "options": {
            "wth": "Hot Water",
            "heat": "Heating",
            "cool": "Cooling",
            "wth_heat": "Hot Water + Heating",
            "wth_cool": "Hot Water + Cooling",
        },
    },
    # Temperature Unit (dp_id: 6) - c, f
    "temp_unit_convert": {
        "dp_id": 6,
        "code": "temp_unit_convert",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "options": {
            "c": "Celsius",
            "f": "Fahrenheit",
        },
    },
}
