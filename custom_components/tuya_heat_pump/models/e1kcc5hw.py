"""Model mapping for e1kcc5hw Tuya Heat Pump."""

MODEL_NAME = "Tuya Heat Pump (e1kcc5hw)"

# ====================================================
# SENSOR TYPES (read-only - accessMode: "ro")
# ====================================================
SENSOR_TYPES = {
    "countdown_left": {
        "dp_id": 14,
        "code": "countdown_left",
        "name": "Mainboard Program",
        "unit": "",
        "icon": "mdi:chip",
        "state_class": "measurement",
        "conversion": "value"
    },
    "temp_current": {
        "dp_id": 16,
        "code": "temp_current",
        "name": "Main Valve Pressure",
        "unit": "P",
        "icon": "mdi:gauge",
        "state_class": "measurement",
        "conversion": "value"
    },
    "power_consumption": {
        "dp_id": 18,
        "code": "power_consumption",
        "name": "Today's Energy",
        "unit": "kWh",
        "icon": "mdi:flash",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100"
    },
    "compressor_strength": {
        "dp_id": 20,
        "code": "compressor_strength",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:cosine-wave",
        "state_class": "measurement",
        "conversion": "value"
    },
    "temp_top": {
        "dp_id": 21,
        "code": "temp_top",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "temp_bottom": {
        "dp_id": 22,
        "code": "temp_bottom",
        "name": "Outlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "coiler_temp": {
        "dp_id": 23,
        "code": "coiler_temp",
        "name": "Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "venting_temp": {
        "dp_id": 24,
        "code": "venting_temp",
        "name": "Exhaust Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "effluent_temp": {
        "dp_id": 25,
        "code": "effluent_temp",
        "name": "Aux Valve Pressure",
        "unit": "P",
        "icon": "mdi:gauge",
        "state_class": "measurement",
        "conversion": "value"
    },
    "around_temp": {
        "dp_id": 26,
        "code": "around_temp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "temp_current_f": {
        "dp_id": 35,
        "code": "temp_current_f",
        "name": "High Pressure Saturation Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "top_temp_f": {
        "dp_id": 36,
        "code": "top_temp_f",
        "name": "Low Pressure Saturation Temp",
        "unit": "°F",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "bottom_temp_f": {
        "dp_id": 37,
        "code": "bottom_temp_f",
        "name": "Internal Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "around_temp_f": {
        "dp_id": 38,
        "code": "around_temp_f",
        "name": "Tank Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "venting_temp_f": {
        "dp_id": 39,
        "code": "venting_temp_f",
        "name": "Water Flow Rate",
        "unit": "L/min",
        "icon": "mdi:water-pump",
        "state_class": "measurement",
        "conversion": "value"
    },
    "effluent_temp_f": {
        "dp_id": 40,
        "code": "effluent_temp_f",
        "name": "Fan Frequency",
        "unit": "Hz",
        "icon": "mdi:fan",
        "state_class": "measurement",
        "conversion": "value"
    },
    "coiler_temp_f": {
        "dp_id": 41,
        "code": "coiler_temp_f",
        "name": "Return Gas Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "cur_current": {
        "dp_id": 102,
        "code": "cur_current",
        "name": "Phase A Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
        "conversion": "value / 1000"
    },
    "voltage_current": {
        "dp_id": 103,
        "code": "voltage_current",
        "name": "Phase A Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "cur_power": {
        "dp_id": 104,
        "code": "cur_power",
        "name": "Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "electric_total": {
        "dp_id": 105,
        "code": "electric_total",
        "name": "Total Energy",
        "unit": "kWh",
        "icon": "mdi:chart-line",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100"
    },
    "eviin": {
        "dp_id": 107,
        "code": "eviin",
        "name": "Economizer Inlet Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "eviout": {
        "dp_id": 108,
        "code": "eviout",
        "name": "Economizer Outlet Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "b_cur": {
        "dp_id": 109,
        "code": "b_cur",
        "name": "Phase B Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
        "conversion": "value / 1000"
    },
    "c_cur": {
        "dp_id": 110,
        "code": "c_cur",
        "name": "Phase C Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
        "conversion": "value / 1000"
    },
    "bv": {
        "dp_id": 111,
        "code": "bv",
        "name": "Phase B Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "cv": {
        "dp_id": 112,
        "code": "cv",
        "name": "Phase C Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "room_temp": {
        "dp_id": 113,
        "code": "room_temp",
        "name": "Room Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    # Hesaplanan sensörler
    "calculated_total_power": {
        "code": "calculated_total_power",
        "name": "Total Power (3-Phase)",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
        "conversion": "value"
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only boolean & bitmap)
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0"  # bitmap, 0 ise hata yok
    },
    "compressor_state": {
        "dp_id": 27,
        "code": "compressor_state",
        "name": "Compressor State",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "backwater": {
        "dp_id": 31,
        "code": "backwater",
        "name": "Hot Water Mode",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "defrost_state": {
        "dp_id": 33,
        "code": "defrost_state",
        "name": "Defrost State",
        "device_class": "cold",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "flag_room_temp": {
        "dp_id": 114,
        "code": "flag_room_temp",
        "name": "Room Temperature Flag",
        "device_class": "problem",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

# ====================================================
# SWITCH TYPES (read-write boolean - accessMode: "rw")
# ====================================================
SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 4,
        "code": "temp_set",
        "name": "Temperature Setpoint",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": -20.0,
        "max_value": 80.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "water_set": {
        "dp_id": 10,
        "code": "water_set",
        "name": "Control Temperature",
        "icon": "mdi:thermometer-water",
        "unit": "L",
        "min_value": 0.0,
        "max_value": 1.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "minitemp_set": {
        "dp_id": 101,
        "code": "minitemp_set",
        "name": "Hot Water Temperature Set",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 80.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "volume_set": {
        "dp_id": 106,
        "code": "volume_set",
        "name": "Power Detection Module",
        "icon": "mdi:meter-electric",
        "unit": "",
        "min_value": 0.0,
        "max_value": 2.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:air-conditioner",
        "options": {
            "cold": "Cooling",
            "heating": "Heating",
            "floor_heating": "Floor Heating",
            "hot_water": "Hot Water",
            "cold_and_hotwater": "Cool & Hot Water",
            "heating_and_hot_water": "Heat & Hot Water",
            "floor_heatign_and_hot_water": "Floor Heat & Hot Water"
        },
        "conversion": "value"
    },
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:cog",
        "options": {
            "ECO": "ECO",
            "Normal": "Normal",
            "Boost": "Boost"
        },
        "conversion": "value"
    },
    "capacity_set": {
        "dp_id": 11,
        "code": "capacity_set",
        "name": "Hot Water Curve Setting",
        "icon": "mdi:chart-line",
        "options": {
            "OFF": "Off",
            "H1": "H1",
            "H2": "H2",
            "H3": "H3",
            "H4": "H4"
        },
        "conversion": "value"
    },
    "countdown_set": {
        "dp_id": 13,
        "code": "countdown_set",
        "name": "Curve Setting",
        "icon": "mdi:timer",
        "options": {
            "OFF": "Off",
            "H1": "H1",
            "H2": "H2",
            "H3": "H3",
            "H4": "H4",
            "H5": "H5",
            "H6": "H6",
            "H7": "H7",
            "H8": "H8",
            "L1": "L1",
            "L2": "L2",
            "L3": "L3",
            "L4": "L4",
            "L5": "L5",
            "L6": "L6",
            "L7": "L7",
            "L8": "L8"
        },
        "conversion": "value"
    },
}
