"""Model mapping for Heat Pump (e1kugiu4)."""

MODEL_NAME = "Heat Pump (e1kugiu4)"

SENSOR_TYPES = {
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
    "inlet_temp": {
        "dp_id": 123,
        "code": "inlet_temp",
        "name": "Hot Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "r_130": {
        "dp_id": 130,
        "code": "r_130",
        "name": "Microcode Version",
        "icon": "mdi:chip",
    },
}

SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 16,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": -10.0,
        "max_value": 85.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "temp_set_1": {
        "dp_id": 124,
        "code": "temp_set_1",
        "name": "Hot Water Target Temperature",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": -10.0,
        "max_value": 85.0,
        "step": 1.0,
        "api_conversion": "value",
    },
}

SELECT_TYPES = {
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "auto": "Auto",
            "cold": "Cooling",
            "hot": "Heating",
            "dhw": "Hot Water",
            "cold_dhw": "Cooling + Hot Water",
            "hot_dhw": "Heating + Hot Water",
        },
    },
}

# --- merge into SENSOR_TYPES (read-only measurements living inside a
# writable raw DP -- accessMode is per-DP not per-field, so these three
# happen to share dp_id 135/140 with genuine setpoints but are actually
# just telemetry readings, not something a user should "set") ---
SENSOR_TYPES = globals().get("SENSOR_TYPES", {})
SENSOR_TYPES.update({
    "invtttemp": {
        "dp_id": 135,
        "code": "invtttemp",
        "raw_source": "r_135",
        "field_index": 41,
        "encoding": "int32_be",
        "conversion": "value / 10",
        "name": "INVT Temperature",
        "unit": "\u00b0C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "input_voltage_frequency_conversion": {
        "dp_id": 135,
        "code": "input_voltage_frequency_conversion",
        "raw_source": "r_135",
        "field_index": 48,
        "encoding": "int32_be",
        "conversion": "value / 10",
        "name": "Input Voltage (Frequency Conversion)",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "ambient_temperature_2": {
        "dp_id": 140,
        "code": "ambient_temperature_2",
        "raw_source": "r_140",
        "field_index": 32,
        "encoding": "int32_be",
        "conversion": "value / 10000",
        "name": "Ambient Temperature?",
        "unit": "\u00b0C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
})

# --- merge into NUMBER_TYPES (contributed by @Schneider006 via raw_explorer.py) ---
# r_141 (dp_id 141) real Tuya name: "03压机设置 & 04风机设置" = "03 Compressor
# Settings & 04 Fan Settings", accessMode "rw" — confirms this is a genuine
# writable setting living under the fan-settings half of this raw DP.
NUMBER_TYPES = globals().get("NUMBER_TYPES", {})
NUMBER_TYPES.update({
    "0428_silentspeedmax": {
        "dp_id": 141,
        "code": "0428_silentspeedmax",
        "raw_source": "r_141",
        "field_index": 37,
        "encoding": "int32_be",
        "step": 1,
        "name": "04.28 SilentSpeedMax",
        "unit": "rpm",
        "icon": "mdi:fan",
    },
})
