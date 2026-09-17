"""Model mapping for Argo Apollo 12HP Air Conditioner (00000048jf)."""

MODEL_NAME = "Argo Apollo 12HP Air Conditioner (00000048jf)"
# ====================================================
# Argo Apollo 12HP @arboeh
# ====================================================
# Monoblock air-to-air unit — mode/fan/swing/etc. below are exposed as
# separate select/switch/sensor entities, same as every other device in
# this integration. There is no climate.py platform here (no device in
# this repo gets a single combined HA "climate" thermostat card with
# hvac_mode/fan_mode/swing_mode) — that would need a new platform to be
# written, not just a model mapping, so it's out of scope for this file.
#
# temp_set_f (dp 24) and temp_current_f (dp 23) are the same physical
# setpoint/reading as temp_set (dp 2) and temp_current (dp 3), just in
# °F — skipped as redundant (temp_unit_convert, dp 19, switches which
# unit the device itself displays/uses, and HA handles unit display on
# its own).
#
# model_type (dp 104, bitmap) is a read-only capability flag telling
# which features this physical variant actually has (bit0 heat+cool,
# bit1 °F-native, bit2 aux heat, bit3 vertical swing, bit4 horizontal
# swing, bit5 purification, bit6 ventilation) — decoded below as a
# sensor. All the DPs it describes (horizontal, anion, etc.) are still
# exposed regardless, since the schema defines them for every unit of
# this model even when a given bit says a specific unit lacks it.

SENSOR_TYPES = {
    "temp_current": {
        "dp_id": 3,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "humidity_current": {
        "dp_id": 18,
        "code": "humidity_current",
        "name": "Current Humidity",
        "unit": "%",
        "icon": "mdi:water-percent",
        "device_class": "humidity",
        "state_class": "measurement",
    },
    # Product Type (dp_id: 104) — capability flags for this physical
    # unit, see header note above.
    "model_type": {
        "dp_id": 104,
        "code": "model_type",
        "name": "Product Type",
        "icon": "mdi:information-outline",
        "conversion": (
            "', '.join(n for b, n in ["
            "(1,'Heat+Cool'),(2,'°F-native'),(4,'Aux Heat'),"
            "(8,'Vertical Swing'),(16,'Horizontal Swing'),"
            "(32,'Purification'),(64,'Ventilation')"
            "] if value & b) or 'None'"
        ),
    },
    # Fault Alarm (dp_id: 108) — plain string, empty when no fault.
    "fault": {
        "dp_id": 108,
        "code": "default",
        "name": "Fault Alarm",
        "icon": "mdi:alert-circle",
        "conversion": "value if value else 'OK'",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 108,
        "code": "default",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value not in ('', None)",
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
    # Eco Mode (dp_id: 8) — cooling mode only, per Tuya's own schema.
    "eco": {
        "dp_id": 8,
        "code": "eco",
        "name": "Eco Mode",
        "icon": "mdi:leaf",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Drying (dp_id: 9) — cool/dry modes only, per Tuya's own schema.
    "drying": {
        "dp_id": 9,
        "code": "drying",
        "name": "Drying",
        "icon": "mdi:water-off",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "ventilation": {
        "dp_id": 10,
        "code": "ventilation",
        "name": "Ventilation",
        "icon": "mdi:air-filter",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "anion": {
        "dp_id": 11,
        "code": "anion",
        "name": "Health/Anion",
        "icon": "mdi:air-purifier",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Auxiliary Heat (dp_id: 12) — heating mode only, per Tuya's own
    # schema.
    "heat": {
        "dp_id": 12,
        "code": "heat",
        "name": "Auxiliary Heat",
        "icon": "mdi:radiator",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "light": {
        "dp_id": 13,
        "code": "light",
        "name": "Display Light",
        "icon": "mdi:led-on",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Sleep (dp_id: 101) — cool/heat modes only, per Tuya's own schema.
    "Sleep": {
        "dp_id": 101,
        "code": "Sleep",
        "name": "Sleep Mode",
        "icon": "mdi:sleep",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Continu (dp_id: 102) — cool/heat modes only, per Tuya's own schema.
    "Continu": {
        "dp_id": 102,
        "code": "Continu",
        "name": "Powerful Mode",
        "icon": "mdi:rocket-launch",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "Silent": {
        "dp_id": 105,
        "code": "Silent",
        "name": "Silent Mode",
        "icon": "mdi:volume-off",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "horizontal": {
        "dp_id": 106,
        "code": "horizontal",
        "name": "Horizontal Swing",
        "icon": "mdi:arrow-left-right",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "vertical": {
        "dp_id": 107,
        "code": "vertical",
        "name": "Vertical Swing",
        "icon": "mdi:arrow-up-down",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 2,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 16.0,
        "max_value": 30.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "humidity_set": {
        "dp_id": 17,
        "code": "humidity_set",
        "name": "Target Humidity",
        "icon": "mdi:water-percent",
        "unit": "%",
        "min_value": 40.0,
        "max_value": 80.0,
        "step": 1.0,
        "api_conversion": "value",
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 4,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "auto": "Auto",
            "cold": "Cooling",
            "hot": "Heating",
            "wet": "Dry",
            "wind": "Fan Only",
        },
    },
    "fan_speed_enum": {
        "dp_id": 5,
        "code": "fan_speed_enum",
        "name": "Fan Speed",
        "icon": "mdi:fan",
        "options": {
            "auto": "Auto",
            "low": "Low",
            "mid": "Medium",
            "high": "High",
        },
    },
    "temp_unit_convert": {
        "dp_id": 19,
        "code": "temp_unit_convert",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "options": {
            "c": "Celsius",
            "f": "Fahrenheit",
        },
    },
}
