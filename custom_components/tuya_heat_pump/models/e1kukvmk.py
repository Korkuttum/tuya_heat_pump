# ====================================================
# Elterm Bulgaria 18CHW-RMS @NAP141, issue #108
# Possible rebrand of AOKOL ASH-18CHW-RKS (unconfirmed)
# Closely related to the "Mango" e1kugiu4 model (different
# modelId, same DP layout for the standard fields and part
# of the raw status block) -- see per-section notes below.
# Power Mode/Silent Mode/Heat Curve select field offsets and
# the full r_135 telemetry block decoded and tested on his
# own unit via raw_explorer.py.
# ====================================================
"""Model mapping for Elterm Bulgaria 18CHW-RMS Heat Pump (e1kukvmk)."""

MODEL_NAME = "Elterm Bulgaria 18CHW-RMS Heat Pump (e1kukvmk)"

SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
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
            "hot": "Heating",
            "dhw": "Hot Water",
            "hot_dhw": "Heating + Hot Water",
            "cold_dhw": "Cooling + Hot Water",
            "cold": "Cooling",
        },
    },
    # --- raw_explorer.py pass by @NAP141 (issue #108): each of these is
    # a 32-bit raw field where only one 16-bit half carries the real
    # value (same "mixed-width field" pattern as e1kugiu4's fan settings
    # below) -- field_index here is already the corrected 16-bit offset,
    # confirmed against his own dump by testing each setting live in the
    # Tuya app and matching which byte changed. ---
    "power_mode": {
        "dp_id": 140,
        "code": "power_mode",
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
    },
    "silent_mode": {
        "dp_id": 140,
        "code": "silent_mode",
        "raw_source": "r_140",
        "field_index": 6,
        "encoding": "int16_be",
        "options": {
            "0": "Disable",
            "1": "Night",
            "2": "AllDay",
        },
        "name": "01.07 Silent Mode",
    },
    "heat_curve": {
        "dp_id": 140,
        "code": "heat_curve",
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
    },
}

NUMBER_TYPES = {
    # Min/max narrowed from the device's generic schema range (-10/85,
    # a shared placeholder, not a real limit for this unit) to the
    # practical range @NAP141 confirmed usable on his own installation.
    "temp_set": {
        "dp_id": 16,
        "code": "temp_set",
        "name": "Target Temp - Heat",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 10.0,
        "max_value": 50.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "temp_set_1": {
        "dp_id": 124,
        "code": "temp_set_1",
        "name": "Target Temp - DHW",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 20.0,
        "max_value": 50.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # raw_explorer.py pass by @NAP141 (issue #108) -- same mixed-width
    # situation as e1kugiu4's fan settings. 40-80 is a compressor
    # inverter frequency ceiling, hence Hz, not rpm (40-80 rpm would be
    # implausibly slow for a running compressor).
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
    "0428_silentspeedmax": {
        "dp_id": 141,
        "code": "0428_silentspeedmax",
        "raw_source": "r_141",
        "field_index": 75,
        "encoding": "int16_be",
        "min_value": 500,
        "max_value": 900,
        "step": 1,
        "name": "04.28 Silent Fan RPM Max",
        "unit": "rpm",
        "icon": "mdi:fan",
    },
}

SENSOR_TYPES = {
    "r_130": {
        "dp_id": 130,
        "code": "r_130",
        "name": "Microcode Version",
        "icon": "mdi:chip",
    },
    # --- dp_id 131-134/154-159: plain Tuya "value" type DPs, not
    # raw-packed, exposed read-only by this device's own cloud schema as
    # "Heat Curve Data 1" through "10" -- read-only visibility
    # alongside the settable `heat_curve` select above. ---
    **{
        f"heat_curve_data_{i}": {
            "dp_id": dp_id,
            "code": f"heat_curve_data_{i}",
            "name": f"Heat Curve Data {i}",
            "icon": "mdi:chart-line",
        }
        for i, dp_id in enumerate([131, 132, 133, 134, 154, 155, 156, 157, 158, 159], start=1)
    },
    # --- dp_id 24/123 (plain "Current Temperature"/"DHW Current
    # Temperature" DPs) dropped: confirmed by @NAP141 to update only
    # ~hourly on his unit, far less useful than the equivalent readings
    # below, which come from the same instantly-updating raw block
    # (r_135) as return/flow temperature. ---
    # --- Full r_135 telemetry block, decoded and tested live against
    # the Tuya app's own status screen by @NAP141 (issue #108) --
    # covers his original request to see compressor/fan target vs.
    # current speed and inlet/outlet temperatures. ---
    "return_temperature": {
        "dp_id": 135,
        "code": "return_temperature",
        "raw_source": "r_135",
        "field_index": 0,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "Water Temp - In Return",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
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
        "name": "Water Temp - Out Flow",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "env_temperature": {
        "dp_id": 135,
        "code": "env_temperature",
        "raw_source": "r_135",
        "field_index": 2,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "Outside Air Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "dhw_temperature": {
        "dp_id": 135,
        "code": "dhw_temperature",
        "raw_source": "r_135",
        "field_index": 3,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "DHW Current Temp",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "tw_wing_temperature": {
        "dp_id": 135,
        "code": "tw_wing_temperature",
        "raw_source": "r_135",
        "field_index": 63,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "Tw Wing Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "tex_exhaust_temp": {
        "dp_id": 135,
        "code": "tex_exhaust_temp",
        "raw_source": "r_135",
        "field_index": 64,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "TEx Exhaust Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ts_suction_temp": {
        "dp_id": 135,
        "code": "ts_suction_temp",
        "raw_source": "r_135",
        "field_index": 65,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "TS Suction Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "comp_target_speed": {
        "dp_id": 135,
        "code": "comp_target_speed",
        "raw_source": "r_135",
        "field_index": 79,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "Compressor Speed Target",
        "unit": "rpm",
        "icon": "mdi:gauge",
    },
    "comp_current_speed": {
        "dp_id": 135,
        "code": "comp_current_speed",
        "raw_source": "r_135",
        "field_index": 80,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "Compressor Speed Current",
        "unit": "rpm",
        "icon": "mdi:gauge",
    },
    "comp_voltage": {
        "dp_id": 135,
        "code": "comp_voltage",
        "raw_source": "r_135",
        "field_index": 81,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "Compressor Voltage DC",
        "unit": "V",
        "device_class": "voltage",
        "state_class": "measurement",
        "icon": "mdi:sine-wave",
    },
    "comp_amps": {
        "dp_id": 135,
        "code": "comp_amps",
        "raw_source": "r_135",
        "field_index": 82,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "Compressor Amps",
        "unit": "A",
        "device_class": "current",
        "state_class": "measurement",
        "icon": "mdi:current-ac",
    },
    "comp_temp": {
        "dp_id": 135,
        "code": "comp_temp",
        "raw_source": "r_135",
        "field_index": 83,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "Compressor Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "comp_power": {
        "dp_id": 135,
        "code": "comp_power",
        "raw_source": "r_135",
        "field_index": 86,
        "encoding": "int16_be",
        "conversion": "value / 100",
        "name": "Compressor Power",
        "unit": "kW",
        "device_class": "power",
        "state_class": "measurement",
        "icon": "mdi:flash",
    },
    "fan_1_target_speed": {
        "dp_id": 135,
        "code": "fan_1_target_speed",
        "raw_source": "r_135",
        "field_index": 87,
        "encoding": "int16_be",
        "name": "Fan1 Speed Target",
        "unit": "rpm",
        "icon": "mdi:fan",
    },
    "fan_1_current_speed": {
        "dp_id": 135,
        "code": "fan_1_current_speed",
        "raw_source": "r_135",
        "field_index": 88,
        "encoding": "int16_be",
        "name": "Fan1 Speed Current",
        "unit": "rpm",
        "icon": "mdi:fan",
    },
    "fan_2_target_speed": {
        "dp_id": 135,
        "code": "fan_2_target_speed",
        "raw_source": "r_135",
        "field_index": 89,
        "encoding": "int16_be",
        "name": "Fan2 Speed Target",
        "unit": "rpm",
        "icon": "mdi:fan",
    },
    "fan_2_current_speed": {
        "dp_id": 135,
        "code": "fan_2_current_speed",
        "raw_source": "r_135",
        "field_index": 90,
        "encoding": "int16_be",
        "name": "Fan2 Speed Current",
        "unit": "rpm",
        "icon": "mdi:fan",
    },
}
