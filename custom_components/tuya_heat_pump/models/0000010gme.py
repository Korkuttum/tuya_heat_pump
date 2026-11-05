"""Model mapping for Smart Thermostat (0000010gme)."""

MODEL_NAME = "Smart Thermostat (0000010gme)"
# ====================================================
# Test Cihazı @korkuttum
# ====================================================

SENSOR_TYPES = {
    # DP 3 (read only): what the thermostat is doing right now. The raw values
    # (no_heating / heating / window_opened) are also used by the climate
    # entity (see CLIMATE_HINTS) to report heating vs idle.
    "work_state": {
        "dp_id": 3,
        "code": "work_state",
        "name": "Working State",
        "icon": "mdi:radiator",
        "conversion": (
            "{'no_heating': 'Idle', 'heating': 'Heating', "
            "'window_opened': 'Window Open'}.get(value, value)"
        ),
    },
    "temp_current": {
        "dp_id": 24,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bitmap - accessMode: "ro")
# ====================================================
# DP 45 is a 6 bit fault bitmap (labels: high_protect, low_protect, int_sensor,
# ext_sensor, battary_low, device_offline); one binary sensor per bit.
BINARY_SENSOR_TYPES = {
    "fault_high_protect": {
        "dp_id": 45,
        "code": "fault",
        "name": "High Temperature Protection",
        "device_class": "problem",
        "icon": "mdi:thermometer-alert",
        "conversion": "(int(value) & 1) != 0",
    },
    "fault_low_protect": {
        "dp_id": 45,
        "code": "fault",
        "name": "Low Temperature Protection",
        "device_class": "problem",
        "icon": "mdi:snowflake-alert",
        "conversion": "(int(value) & 2) != 0",
    },
    "fault_int_sensor": {
        "dp_id": 45,
        "code": "fault",
        "name": "Internal Sensor Fault",
        "device_class": "problem",
        "icon": "mdi:alert-circle",
        "conversion": "(int(value) & 4) != 0",
    },
    "fault_ext_sensor": {
        "dp_id": 45,
        "code": "fault",
        "name": "External Sensor Fault",
        "device_class": "problem",
        "icon": "mdi:alert-circle",
        "conversion": "(int(value) & 8) != 0",
    },
    "fault_battary_low": {
        "dp_id": 45,
        "code": "fault",
        "name": "Battery Low",
        "device_class": "battery",
        "icon": "mdi:battery-alert",
        "conversion": "(int(value) & 16) != 0",
    },
    "fault_device_offline": {
        "dp_id": 45,
        "code": "fault",
        "name": "Device Offline Alarm",
        "device_class": "problem",
        "icon": "mdi:lan-disconnect",
        "conversion": "(int(value) & 32) != 0",
    },
}

# ====================================================
# SWITCH TYPES (read-write bool - accessMode: "rw")
# ====================================================
SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # DP 10: frost protection (keeps the room above a minimum temperature
    # even while the thermostat is switched off).
    "frost": {
        "dp_id": 10,
        "code": "frost",
        "name": "Frost Protection",
        "icon": "mdi:snowflake-thermometer",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "factory_reset": {
        "dp_id": 39,
        "code": "factory_reset",
        "name": "Factory Reset",
        "icon": "mdi:restore",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "child_lock": {
        "dp_id": 40,
        "code": "child_lock",
        "name": "Child Lock",
        "icon": "mdi:lock",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 16,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 100.0,
        "step": 0.5,
        "conversion": "value / 10",
        "api_conversion": "int(value * 10)",
    },
    "upper_temp": {
        "dp_id": 19,
        "code": "upper_temp",
        "name": "Upper Temperature Limit",
        "icon": "mdi:thermometer-chevron-up",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 100.0,
        "step": 0.5,
        "conversion": "value / 10",
        "api_conversion": "int(value * 10)",
    },
    "lower_temp": {
        "dp_id": 26,
        "code": "lower_temp",
        "name": "Lower Temperature Limit",
        "icon": "mdi:thermometer-chevron-down",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 100.0,
        "step": 0.5,
        "conversion": "value / 10",
        "api_conversion": "int(value * 10)",
    },
    "temp_correction": {
        "dp_id": 27,
        "code": "temp_correction",
        "name": "Temperature Correction",
        "icon": "mdi:thermometer-lines",
        "unit": "°C",
        "min_value": -10.0,
        "max_value": 10.0,
        "step": 0.5,
        "conversion": "value / 10",
        "api_conversion": "int(value * 10)",
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
        "icon": "mdi:hvac",
        "options": {
            "manual": "Manual",
            "eco": "Eco",
            "auto": "Auto",
        },
    },
}

# ====================================================
# CLIMATE HINTS (optional, read by model_loader.py / climate.py / config_flow.py)
#
# A real room thermostat runs its own closed loop, so the climate entity only
# mirrors it: power switch on = heat, off = off; the target is written to the
# device. These hints add what the generic climate bridge cannot guess:
#   defaults        pre-selected DPs for the climate form
#   default_enabled the climate form is pre-ticked for new setups
#   action          DP + raw values telling whether it is really heating
#   preset          select DP whose raw values become HA presets
# Models without CLIMATE_HINTS behave exactly as before.
# ====================================================
CLIMATE_HINTS = {
    "default_enabled": True,
    "defaults": {
        "power": "switch",
        "current": "temp_current",
        "target": "temp_set",
    },
    "action": {
        "code": "work_state",
        "heating": ["heating"],
        "idle": ["no_heating", "window_opened"],
    },
    "preset": {
        "code": "mode",
        "values": ["manual", "eco", "auto"],
    },
}
