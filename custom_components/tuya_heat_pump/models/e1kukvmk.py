# ====================================================
# Elterm 18CHW-RMS @NAP141, issue #108
# Possible rebrand of AOKOL ASH-18CHW-RKS (unconfirmed)
# Closely related to the "Mango" e1kugiu4 model (different
# modelId, same DP layout for the standard fields and part
# of the raw status block -- see notes below).
# ====================================================
"""Model mapping for Elterm 18CHW-RMS Heat Pump (e1kukvmk)."""

MODEL_NAME = "Elterm 18CHW-RMS Heat Pump (e1kukvmk)"

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

# --- merge into SENSOR_TYPES (dp_id 131-134/154-159 -- plain Tuya
# "value" type DPs, not raw-packed, exposed read-only by this device's
# own cloud schema as "Heat Curve Data 1" through "10" -- covers part
# of @NAP141's 01.47 HEAT_CURVE request as read-only visibility; all
# ten read 0 on his unit with Heat Curve presumably inactive) ---
SENSOR_TYPES = globals().get("SENSOR_TYPES", {})
SENSOR_TYPES.update({
    f"heat_curve_data_{i}": {
        "dp_id": dp_id,
        "code": f"heat_curve_data_{i}",
        "name": f"Heat Curve Data {i}",
        "icon": "mdi:chart-line",
    }
    for i, dp_id in enumerate([131, 132, 133, 134, 154, 155, 156, 157, 158, 159], start=1)
})

# --- merge into SENSOR_TYPES (ported from the sibling e1kugiu4 model --
# r_135 field_index 0/1 as int16_be /10 decode to 43.0°C / 42.9°C on
# @NAP141's own dump (issue #108), a sane return/flow pair alongside his
# temp_current=41.1°C / temp_set=41°C in heating mode, so this part of
# the raw layout carries over to this modelId) ---
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

# --- merge into SENSOR_TYPES (ported from e1kugiu4, same "?" caveat --
# r_140 field_index 32 as int32_be /10000 decodes to a plausible-looking
# ~32.8°C on @NAP141's dump, but e1kugiu4's own notes already flag this
# field as unconfirmed; e1kugiu4's alternative, more trustworthy ambient
# reading (data_tunnel_2 byte_offset 93) decodes to garbage (0.1°C) on
# this modelId -- that record's byte layout depends on variable-length
# labels earlier in the packet and does not carry over -- so this is the
# only ambient candidate kept here) ---
SENSOR_TYPES = globals().get("SENSOR_TYPES", {})
SENSOR_TYPES.update({
    "ambient_temperature_2": {
        "dp_id": 140,
        "code": "ambient_temperature_2",
        "raw_source": "r_140",
        "field_index": 32,
        "encoding": "int32_be",
        "conversion": "value / 10000",
        "name": "Ambient Temperature?",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
})

# --- merge into NUMBER_TYPES (ported from e1kugiu4 -- r_141 covers "03
# Compressor Settings & 04 Fan Settings"; these two fan-side fields
# decode to plausible values on @NAP141's dump (800 and 700, both well
# inside the ranges below), matching his own report that copy-pasting
# e1kugiu4's 04.28 field already worked for fan speed on this device.
# His other requests -- 03.07 Max RPS and 03.42 SilentFreqMax -- live
# in the still-unmapped "03 Compressor Settings" half of this same raw
# DP and need a fresh raw_explorer.py pass to locate) ---
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

# --- merge into NUMBER_TYPES (@NAP141's own raw_explorer.py pass, issue
# #108 -- same "mixed-width field" situation as 0403fanmaxcool/
# 0428silentspeedmax above: raw_explorer auto-detected this as ONE
# int32_be field at r_141 field_index 20, but he confirmed by testing
# that only the lower 16 bits carry the real value (the upper half reads
# 10, well outside 40-80; the lower half reads 40, right at his tested
# minimum) -- so it's split into a proper int16_be field (int32 index 20
# -> byte offset 80-81 -> int16 field_index 41) instead of the single
# misleading int32 reading) ---
NUMBER_TYPES = globals().get("NUMBER_TYPES", {})
NUMBER_TYPES.update({
    "0342_silentfreqmax": {
        "dp_id": 141,
        "code": "0342_silentfreqmax",
        "raw_source": "r_141",
        "field_index": 41,
        "encoding": "int16_be",
        "min_value": 40,
        "max_value": 80,
        "step": 1,
        "name": "03.42 SilentFreqMax",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
    },
})

# --- merge into SELECT_TYPES (@NAP141's own raw_explorer.py pass, issue
# #108 -- same mixed-width situation again, this time in r_140 ("01 User
# Parameters"). raw_explorer auto-detected each as ONE int32_be field;
# he confirmed by testing in the Tuya app which 16-bit half of each
# actually holds the value (checked here against his own dump too --
# the other half reads out of range or less plausible in each case):
#   - 01.06 Power Mode: int32 field_index 2, real value in the LOWER
#     half (byte offset 10-11 -> int16 field_index 5; reads 2 = "Silent",
#     in range, vs. 25 out of range on the other half)
#   - 01.07 Mode Silent: int32 field_index 3, real value in the UPPER
#     half (byte offset 12-13 -> int16 field_index 6; reads 0 = "Disable",
#     in range, vs. 22 out of range on the other half) -- not one of his
#     four requested items, but came out of the same pass
#   - 01.47 Heat Curve: int32 field_index 23, real value in the UPPER
#     half (byte offset 92-93 -> int16 field_index 46; reads 14 =
#     "CURVE#6H", a plausible active selection, vs. 0 on the other half)
# ---
SELECT_TYPES = globals().get("SELECT_TYPES", {})
SELECT_TYPES.update({
    "0106_power_mode": {
        "dp_id": 140,
        "code": "0106_power_mode",
        "raw_source": "r_140",
        "field_index": 5,
        "encoding": "int16_be",
        "options": {
            "0": "Standard",
            "1": "Strong",
            "2": "Silent",
            "3": "Auto",
        },
        "name": "01.06 Power Mode",
        "icon": "mdi:tune",
    },
    "0107_mode_silent": {
        "dp_id": 140,
        "code": "0107_mode_silent",
        "raw_source": "r_140",
        "field_index": 6,
        "encoding": "int16_be",
        "options": {
            "0": "Disable",
            "1": "Night",
            "2": "AllDay",
        },
        "name": "01.07 Mode Silent",
        "icon": "mdi:volume-mute",
    },
    "0147_heat_curve": {
        "dp_id": 140,
        "code": "0147_heat_curve",
        "raw_source": "r_140",
        "field_index": 46,
        "encoding": "int16_be",
        "options": {
            "0": "DISABLE",
            "1": "CURVE#1L",
            "2": "CURVE#2L",
            "3": "CURVE#3L",
            "4": "CURVE#4L",
            "5": "CURVE#5L",
            "6": "CURVE#6L",
            "7": "CURVE#7L",
            "8": "CURVE#8L",
            "9": "CURVE#1H",
            "10": "CURVE#2H",
            "11": "CURVE#3H",
            "12": "CURVE#4H",
            "13": "CURVE#5H",
            "14": "CURVE#6H",
            "15": "CURVE#7H",
            "16": "CURVE#8H",
            "17": "CURVE#9",
        },
        "name": "01.47 Heat Curve",
        "icon": "mdi:chart-line",
    },
})
