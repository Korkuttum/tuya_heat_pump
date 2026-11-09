# ====================================================
# Energie Aquapura Monobloc 270ix @mail467, issue #114
# Tuya modelId: 000004bw48
# A heat pump WATER HEATER (hot water cylinder), not a space
# heating unit. Every DP in the cloud schema is a plain
# bool/value/enum, so no raw decoding is needed.
#
# Not exposed on purpose:
#   - temp_2 / temp_3 / temp_4 (dp 106-108): read -1000 on the
#     reported unit, i.e. probes that are not connected.
#   - hpw1/hpw2/hpwd1/hpwd2 (dp 140-143): weekly timer tables,
#     raw and not decoded.
#   - dev_config / soft_versions / get_consumptions /
#     consumptions / consumptions_values: raw blobs.
#   - reset_params (dp 124): would wipe the unit's parameters.
#   - capp_select / chrono_*_ctrl (dp 161-164): purpose unknown.
#   - temp_current (dp 16) and temp_current_f (dp 35): the
#     schema calls them "temp_error_crit" and "Logo_Change",
#     they are not temperatures.
# ====================================================
"""Model mapping for Energie Aquapura Monobloc 270ix (000004bw48)."""

MODEL_NAME = "Energie Aquapura Monobloc 270ix (000004bw48)"

# State sensors report the unit's own words ("enabled", "active", ...).
# They are plain text sensors on purpose: Home Assistant's "enum" device
# class would need a fixed option list for every one of them.
SENSOR_TYPES = {
    "temp_1": {
        # Temp Prob 1, 0-85. 53 on the reported unit while the heater was
        # idle, so most likely the cylinder temperature.
        "dp_id": 105,
        "code": "temp_1",
        "name": "Temperature Probe 1",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "comp_power": {
        # Cloud schema: scale 3, unit kWh, 0-5000 (i.e. up to 5 kWh).
        "dp_id": 160,
        "code": "comp_power",
        "name": "Compressor Energy",
        "unit": "kWh",
        "icon": "mdi:flash",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 1000",
    },
    "res_power": {
        "dp_id": 159,
        "code": "res_power",
        "name": "Resistor Energy",
        "unit": "kWh",
        "icon": "mdi:flash",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 1000",
    },
    "comp": {
        # disabled / enabled / timer / active / lp / hp / temp / lat / df
        "dp_id": 114,
        "code": "comp",
        "name": "Compressor State",
        "icon": "mdi:heat-pump",
    },
    "res": {
        # disabled / enabled / timer / active / tc / ma / ta
        "dp_id": 115,
        "code": "res",
        "name": "Resistor State",
        "icon": "mdi:radiator",
    },
    "hp_state": {
        "dp_id": 156,
        "code": "hp_state",
        "name": "HP State",
        "icon": "mdi:heat-pump-outline",
    },
    "cp_state": {
        "dp_id": 157,
        "code": "cp_state",
        "name": "CP State",
        "icon": "mdi:information-outline",
    },
    "vp_state": {
        # disabled / enabled / loading / active
        "dp_id": 165,
        "code": "vp_state",
        "name": "VP State",
        "icon": "mdi:information-outline",
    },
    "disinfect": {
        # disabled / enabled / active
        "dp_id": 128,
        "code": "disinfect",
        "name": "Disinfection State",
        "icon": "mdi:shield-check",
    },
    "caux": {
        # disabled / enabled / timer / active / error
        "dp_id": 139,
        "code": "caux",
        "name": "Auxiliary Contact",
        "icon": "mdi:electric-switch",
    },
    "vwd3": {
        # Cloud name "Log_list": ERR_NONE, ERR_01_S1 ... ERR_42_PV.
        # The reported unit shows ERR_13_S3 (timestamp from 2025), so this
        # may be the last logged error rather than a live one.
        "dp_id": 155,
        "code": "vwd3",
        "name": "Error Log",
        "icon": "mdi:alert-circle-outline",
    },
}

# Binary Sensor Types - read-only booleans
BINARY_SENSOR_TYPES = {
    "pv": {
        "dp_id": 113,
        "code": "pv",
        "name": "Photovoltaic Mode",
        "device_class": "running",
        "icon": "mdi:solar-power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# Switch Types - read-write booleans
SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "comp_cmd": {
        "dp_id": 111,
        "code": "comp_cmd",
        "name": "Compressor Order",
        "icon": "mdi:heat-pump",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "res_cmd": {
        "dp_id": 112,
        "code": "res_cmd",
        "name": "Resistor Order",
        "icon": "mdi:radiator",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "dis_cmd": {
        "dp_id": 129,
        "code": "dis_cmd",
        "name": "Disinfection Order",
        "icon": "mdi:shield-check",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "vstate": {
        "dp_id": 126,
        "code": "vstate",
        "name": "Vacation Mode",
        "icon": "mdi:beach",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# Number Types - read-write values. Ranges are the ones the cloud schema
# publishes; none of them has been confirmed on a unit yet.
NUMBER_TYPES = {
    "temp_set": {
        # Reads 10 on the reported unit with a 2023 timestamp, so it may not
        # be the setpoint the Tuya app shows (P01 below is the other
        # candidate).
        "dp_id": 4,
        "code": "temp_set",
        "name": "Temperature Setpoint",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 10.0,
        "max_value": 120.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "p01": {
        "dp_id": 116,
        "code": "p01",
        "name": "P01 Compressor Setpoint",
        "icon": "mdi:thermometer-water",
        "unit": "°C",
        "min_value": 10.0,
        "max_value": 60.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "h01": {
        "dp_id": 117,
        "code": "h01",
        "name": "H01 Compressor Differential",
        "icon": "mdi:thermometer-lines",
        "unit": "°C",
        "min_value": 2.0,
        "max_value": 20.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "p02": {
        "dp_id": 118,
        "code": "p02",
        "name": "P02 Electric Heater Setpoint",
        "icon": "mdi:thermometer-water",
        "unit": "°C",
        "min_value": 10.0,
        "max_value": 65.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "h02": {
        "dp_id": 119,
        "code": "h02",
        "name": "H02 Electric Heater Differential",
        "icon": "mdi:thermometer-lines",
        "unit": "°C",
        "min_value": 2.0,
        "max_value": 20.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "p01_pv": {
        "dp_id": 120,
        "code": "p01_pv",
        "name": "P01 PV Compressor Setpoint",
        "icon": "mdi:solar-power",
        "unit": "°C",
        "min_value": 1.0,
        "max_value": 60.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "h01_pv": {
        "dp_id": 121,
        "code": "h01_pv",
        "name": "H01 PV Compressor Differential",
        "icon": "mdi:solar-power",
        "unit": "°C",
        "min_value": 2.0,
        "max_value": 20.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "p02_pv": {
        "dp_id": 122,
        "code": "p02_pv",
        "name": "P02 PV Electric Heater Setpoint",
        "icon": "mdi:solar-power",
        "unit": "°C",
        "min_value": 1.0,
        "max_value": 65.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "h02_pv": {
        "dp_id": 123,
        "code": "h02_pv",
        "name": "H02 PV Electric Heater Differential",
        "icon": "mdi:solar-power",
        "unit": "°C",
        "min_value": 2.0,
        "max_value": 20.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "vac_days": {
        "dp_id": 158,
        "code": "vac_days",
        "name": "Vacation Days",
        "icon": "mdi:calendar-range",
        "unit": "d",
        "min_value": 2.0,
        "max_value": 99.0,
        "step": 1.0,
        "api_conversion": "value",
    },
}

# Select Types - read-write enums
SELECT_TYPES = {
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:cog",
        "options": {
            "NA": "NA",
            "Eco": "Eco",
            "Auto": "Auto",
            "Boost": "Boost",
        },
    },
}
