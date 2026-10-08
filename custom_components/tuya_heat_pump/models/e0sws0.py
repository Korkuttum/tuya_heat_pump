"""Model mapping for NMT MIA13 (e0sws0)."""

MODEL_NAME = "NMT MIA13 (e0sws0)"
# ====================================================
# NMT MIA13 @MrIcemanLE (issue #97)
# https://nmt-systeme.com/waermepumpen/mia/
# ====================================================
# The Tuya schema is a generic template for up to 3 heating circuits +
# a DHW tank; this reporter's unit only has Circuit 1 wired up, so Circuit 2,
# Circuit 3 and Hot Water entities below will read -20.0 °C (Tuya's
# "no sensor connected" sentinel value) and stay off on installs that
# don't use them -- harmless, just ignore/disable those entities.
#
# IMPORTANT -- this device reuses Tuya's generic dp codes with
# DIFFERENT real meanings (confirmed against the vendor app UI by the
# reporter), so the `code` strings below are kept as-is for the API
# but `name` reflects the real, confirmed meaning:
#   - dp 9  "child_lock"      is actually Circuit 2 On/Off (NOT a child lock)
#   - dp 10 "work_power"      is actually Circuit 2 Current Temperature
#   - dp 15 "upper_temp"      is actually Hot Water (DHW) Setpoint
#   - dp 16 "lower_temp"      is actually Circuit 2 Setpoint
#   - dp 19 "temp_correction" is actually Circuit 3 Setpoint (NOT a correction factor)
#   - dp 112 "switch_led"     is actually Circuit 3 On/Off
#   - dp 113 "temp_indoor"    is actually Circuit 3 Current Temperature
#   - dp 115 "temp_outdoor"   is actually Hot Water Tank Temperature (NOT outdoor temp)
#
# buffer_top_temp has no standalone Tuya dp of its own -- it only
# exists inside the raw "zone1_func_info" block (dp 106), a 139-byte
# record pushed independently roughly every 3.2 seconds regardless of
# whether the vendor app is open (confirmed via a 66s idle capture),
# so it's safe to poll. Field offset confirmed against the app's own
# status page (int16_be, byte 28-29, value / 10).
#
# NOT included: dp 101-111/116-140's other raw blocks and the
# "mod_stat_data_00..15" group in particular. These behave like the
# shared paged status/parameter menu protocol also seen on the Mango
# Energy model (issue #90) -- the reporter's own decoded catalog shows
# the SAME logical reading (e.g. room/outdoor/buffer temperature)
# arriving on a DIFFERENT dp_id each time depending on which app screen
# was open, so there is no fixed, reliable dp/offset to bind a sensor
# to. Revisit only if someone confirms a way to read a specific page
# on demand (e.g. via a local-mode command) independent of the app.
#
# version_info (dp 101) and system_info (dp 102) contain plain
# firmware/hardware version text but weren't confirmed/needed for this
# report -- left out for now.
#
# circuit1_setpoint_raw (added per @MrIcemanLE, PR #99): on this unit
# the plain DP temp_set (dp 2) only ever reads the -20 placeholder, so
# the Heating Circuit 1 Setpoint number entity above can't show the
# real value. The live setpoint (58 degC, matching the app) is in the
# same zone1_func_info block as buffer_top_temp, read-only here since
# writing it would need the raw field path, not plain dp 2.

SENSOR_TYPES = {
    "circuit1_current_temp": {
        "dp_id": 3,
        "code": "temp_current",
        "name": "Heating Circuit 1 Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "circuit2_current_temp": {
        "dp_id": 10,
        "code": "work_power",
        "name": "Heating Circuit 2 Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "circuit3_current_temp": {
        "dp_id": 113,
        "code": "temp_indoor",
        "name": "Heating Circuit 3 Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "hot_water_tank_temp": {
        "dp_id": 115,
        "code": "temp_outdoor",
        "name": "Hot Water Tank Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "buffer_top_temp": {
        "dp_id": 106,
        "code": "buffer_top_temp",
        "raw_source": "zone1_func_info",
        "field_index": 14,  # byte offset 28-29
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "Buffer Top Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "circuit1_setpoint_raw": {
        "dp_id": 106,
        "code": "circuit1_setpoint_raw",
        "raw_source": "zone1_func_info",
        "field_index": 7,  # byte offset 14-15
        "encoding": "int16_be",
        "conversion": "value",
        "name": "Heating Circuit 1 Setpoint Reading",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
}

BINARY_SENSOR_TYPES = {}

SWITCH_TYPES = {
    "circuit1_power": {
        "dp_id": 1,
        "code": "switch",
        "name": "Heating Circuit 1 Power",
        "icon": "mdi:power",
    },
    "circuit2_power": {
        "dp_id": 9,
        "code": "child_lock",
        "name": "Heating Circuit 2 Power",
        "icon": "mdi:power",
    },
    "circuit3_power": {
        "dp_id": 112,
        "code": "switch_led",
        "name": "Heating Circuit 3 Power",
        "icon": "mdi:power",
    },
    "hot_water_power": {
        "dp_id": 114,
        "code": "hot_switch",
        "name": "Hot Water Power",
        "icon": "mdi:water-boiler",
    },
}

NUMBER_TYPES = {
    "circuit1_setpoint": {
        "dp_id": 2,
        "code": "temp_set",
        "name": "Heating Circuit 1 Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": -20.0,
        "max_value": 85.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "circuit2_setpoint": {
        "dp_id": 16,
        "code": "lower_temp",
        "name": "Heating Circuit 2 Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": -20.0,
        "max_value": 85.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "circuit3_setpoint": {
        "dp_id": 19,
        "code": "temp_correction",
        "name": "Heating Circuit 3 Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": -20.0,
        "max_value": 85.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "hot_water_setpoint": {
        "dp_id": 15,
        "code": "upper_temp",
        "name": "Hot Water Setpoint",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 80.0,
        "step": 1.0,
        "api_conversion": "value",
    },
}

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
        },
    },
}

TEXT_TYPES = {}
