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
#
# Both fields below were originally auto-detected as int32_be (r_141's
# overall payload alignment), but each is actually a 16-bit value packed
# inside one 32-bit slot — raw_explorer picks one encoding for the whole
# DP, so a mixed-width field like this reads as a misleadingly large
# number (e.g. 66036 instead of 500). Confirmed by checking the upper/
# lower 16 bits of the two sample values Schneider006 captured: they
# match his requested display ranges exactly (500/900 and 0/2000), so
# encoding was corrected to int16_be with a recalculated field_index
# (int32 byte offset ÷ 2, landing on whichever half held the real value).
NUMBER_TYPES = globals().get("NUMBER_TYPES", {})
NUMBER_TYPES.update({
    "0428_silentspeedmax": {
        "dp_id": 141,
        "code": "0428_silentspeedmax",
        "raw_source": "r_141",
        "field_index": 75,
        "encoding": "int16_be",
        "min_value": 500,
        "max_value": 900,
        "step": 1,
        "name": "04.28 SilentSpeedMax",
        "unit": "rpm",
        "icon": "mdi:fan",
    },
    "0403fanmaxcool": {
        "dp_id": 141,
        "code": "0403fanmaxcool",
        "raw_source": "r_141",
        "field_index": 50,
        "encoding": "int16_be",
        "min_value": 0,
        "max_value": 2000,
        "step": 1,
        "name": "04.03 FanMaxCool",
        "unit": "rpm",
        "icon": "mdi:fan",
    },
})

# --- merge into SENSOR_TYPES (contributed by @Schneider006 via raw_explorer.py) ---
# raw_explorer auto-detected this as ONE int32_be field (field_index 0
# of r_135), but Schneider006 confirmed by testing that it's actually
# TWO packed int16 temperatures — same "mixed-width field" situation
# as SilentSpeedMax/FanMaxCool above. Per his description: upper 16
# bits = return temperature (Rücklauf), lower 16 bits = flow/supply
# temperature (Vorlauf). Split into two proper int16_be fields
# (byte offset 0-1 and 2-3 -> int16 field_index 0 and 1) instead of
# the single misleading int32 reading.
SENSOR_TYPES = globals().get("SENSOR_TYPES", {})
SENSOR_TYPES.update({
    "return_temperature": {
        "dp_id": 135,
        "code": "return_temperature",
        "raw_source": "r_135",
        "field_index": 0,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "Return Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "flow_temperature": {
        "dp_id": 135,
        "code": "flow_temperature",
        "raw_source": "r_135",
        "field_index": 1,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "Flow Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
})
