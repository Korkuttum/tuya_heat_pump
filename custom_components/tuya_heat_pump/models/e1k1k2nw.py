"""Model mapping for Aquastrong Pool Heat Pump (e1k1k2nw)."""

MODEL_NAME = "Aquastrong Pool Heat Pump (e1k1k2nw)"
# ====================================================
# Aquastrong @lmatter
# ====================================================
SENSOR_TYPES = {
    # Inlet Water Temperature / Pool Temperature (dp_id: 21)
    "temp_top": {
        "dp_id": 21,
        "code": "temp_top",
        "name": "In Water Temperature",
        "unit": "°F",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Outlet Water Temperature (dp_id: 22)
    "temp_bottom": {
        "dp_id": 22,
        "code": "temp_bottom",
        "name": "Out Water Temperature",
        "unit": "°F",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Ambient Air Temperature (dp_id: 26)
    "around_temp": {
        "dp_id": 26,
        "code": "around_temp",
        "name": "Ambient Temperature",
        "unit": "°F",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Compressor Frequency (dp_id: 20)
    "compressor_strength": {
        "dp_id": 20,
        "code": "compressor_strength",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:engine",
        "state_class": "measurement",
    },
    # Coiler Temperature (dp_id: 23)
    "coiler_temp": {
        "dp_id": 23,
        "code": "coiler_temp",
        "name": "Coiler Temperature",
        "unit": "°F",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Venting / Discharge Temperature (dp_id: 24)
    "venting_temp": {
        "dp_id": 24,
        "code": "venting_temp",
        "name": "Discharge Temperature",
        "unit": "°F",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # EEV Position - Electronic Expansion Valve (dp_id: 16)
    # NOTE: This is NOT a temperature despite the "P" unit - it is valve position in pulses
    "temp_current": {
        "dp_id": 16,
        "code": "temp_current",
        "name": "EEV Position",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    # Power Consumption - cumulative kWh (dp_id: 18) scale: 2 (divide by 100)
    "power_consumption": {
        "dp_id": 18,
        "code": "power_consumption",
        "name": "AC Total Energy",
        "unit": "kWh",
        "icon": "mdi:lightning-bolt",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100",
    },
    # Current Power Draw in Watts (dp_id: 104) scale: 1 (divide by 10)
    "cur_power": {
        "dp_id": 104,
        "code": "cur_power",
        "name": "AC Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    # Current (Amps) (dp_id: 102) scale: 3 (divide by 1000)
    "cur_current": {
        "dp_id": 102,
        "code": "cur_current",
        "name": "Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
        "conversion": "value / 1000",
    },
    # Voltage (dp_id: 103) scale: 1 (divide by 10)
    "voltage_current": {
        "dp_id": 103,
        "code": "voltage_current",
        "name": "Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt-circle",
        "device_class": "voltage",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    # Total Energy (dp_id: 105) scale: 2 (divide by 100)
    "electric_total": {
        "dp_id": 105,
        "code": "electric_total",
        "name": "Total Energy",
        "unit": "kWh",
        "icon": "mdi:counter",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100",
    },
    # Fault bitmap (dp_id: 15)
    "fault_code": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Code",
        "icon": "mdi:alert-circle",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    # Compressor State (dp_id: 27)
    "compressor_state": {
        "dp_id": 27,
        "code": "compressor_state",
        "name": "Compressor Running",
        "icon": "mdi:engine",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Defrost State (dp_id: 33)
    "defrost_state": {
        "dp_id": 33,
        "code": "defrost_state",
        "name": "Defrost Active",
        "icon": "mdi:snowflake-melt",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Fault Status (dp_id: 15)
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Protection Status",
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
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    # Target Temperature Setpoint (dp_id: 4) - native °F, range 41-104
    "temp_set": {
        "dp_id": 4,
        "code": "temp_set",
        "name": "Heat Temperature",
        "icon": "mdi:thermostat",
        "unit": "°F",
        "min_value": 41.0,
        "max_value": 104.0,
        "step": 1.0,
        "conversion": "int(value)",
        "api_conversion": "int(value)",
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    # Mode (dp_id: 2) - make_cold, make_hot, auto
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Work Mode",
        "icon": "mdi:hvac",
        "options": {
            "make_cold": "Cool",
            "make_hot": "Heat",
            "auto": "Auto",
        },
    },
    # Work Mode (dp_id: 5) - ECO, Normal, Boost
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Performance Mode",
        "icon": "mdi:cog",
        "options": {
            "ECO": "ECO",
            "Normal": "Normal",
            "Boost": "Boost",
        },
    },
}
