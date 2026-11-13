# ====================================================
# MyCond BeeHeat @mpyzhov, issue #118
# Tuya modelId: 0000043th5
# Air-to-water heat pump: heating, cooling, domestic hot water
# and a second zone. All data points of the cloud schema are plain
# bool / value / enum, no raw decoding is needed. Temperatures are
# sent in tenths of a degree (scale 1).
#
# Not exposed on purpose:
#   - dp 131-151: the allowed minimum / maximum of every setpoint
#     (read-only). They are used as the number ranges below.
#   - dp 152-157 and 180 (twc_*, no_twc_*, auto_run_tar_mode):
#     installer configuration values of unknown meaning.
#   - Setpoint names for dp 105 and dp 158 are inferred from the
#     zone 2 names (auto cooling / auto heating) and are not
#     confirmed on a unit yet.
# ====================================================
"""Model mapping for MyCond BeeHeat (0000043th5)."""

MODEL_NAME = "MyCond BeeHeat (0000043th5)"

# Sensor Types - read-only
SENSOR_TYPES = {
    "in_water_temp": {
        "dp_id": 106,
        "code": "in_water_temp",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "out_water_temp": {
        "dp_id": 107,
        "code": "out_water_temp",
        "name": "Outlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "tank_temp": {
        "dp_id": 108,
        "code": "tank_temp",
        "name": "Tank Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "amb_temp": {
        "dp_id": 118,
        "code": "amb_temp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "disc_temp": {
        "dp_id": 119,
        "code": "disc_temp",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "back_temp": {
        "dp_id": 120,
        "code": "back_temp",
        "name": "Return Gas Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "tidr": {
        "dp_id": 181,
        "code": "tidr",
        "name": "Indoor Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer-outline",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "comp_freq": {
        "dp_id": 121,
        "code": "comp_freq",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
    },
    "m_eev": {
        "dp_id": 122,
        "code": "m_eev",
        "name": "Main EEV Position",
        "unit": "step",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "a_eev": {
        "dp_id": 123,
        "code": "a_eev",
        "name": "Auxiliary EEV Position",
        "unit": "step",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "dc_fan1": {
        "dp_id": 125,
        "code": "dc_fan1",
        "name": "DC Fan 1 Speed",
        "unit": "RPM",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    "dc_fan2": {
        "dp_id": 126,
        "code": "dc_fan2",
        "name": "DC Fan 2 Speed",
        "unit": "RPM",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    "flow_rate": {
        "dp_id": 127,
        "code": "flow_rate",
        "name": "Water Flow Rate",
        "unit": "m³/h",
        "icon": "mdi:water-pump",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "ac_vol": {
        "dp_id": 128,
        "code": "ac_vol",
        "name": "AC Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "ac_curr": {
        "dp_id": 129,
        "code": "ac_curr",
        "name": "AC Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "ac_fan": {
        # close / low_spd / high_spd
        "dp_id": 124,
        "code": "ac_fan",
        "name": "AC Fan State",
        "icon": "mdi:fan",
    },
}

# Binary Sensor Types - read-only
BINARY_SENSOR_TYPES = {
    "fault": {
        # Bitmap, 0 = no fault. Individual bits are not decoded.
        "dp_id": 6,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    "fault_flag": {
        "dp_id": 130,
        "code": "fault_flag",
        "name": "Fault Flag",
        "device_class": "problem",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "protect_flag": {
        "dp_id": 110,
        "code": "protect_flag",
        "name": "Protection Active",
        "icon": "mdi:shield-alert",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "freeze": {
        "dp_id": 114,
        "code": "freeze",
        "name": "Anti-Freeze Active",
        "icon": "mdi:snowflake-alert",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "defrost": {
        "dp_id": 115,
        "code": "defrost",
        "name": "Defrost Active",
        "icon": "mdi:snowflake-melt",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "pump_sta": {
        "dp_id": 116,
        "code": "pump_sta",
        "name": "Water Pump Running",
        "icon": "mdi:pump",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "valve": {
        "dp_id": 117,
        "code": "valve",
        "name": "Valve Open",
        "icon": "mdi:valve",
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
    "mute": {
        "dp_id": 101,
        "code": "mute",
        "name": "Silent Mode",
        "icon": "mdi:volume-off",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "holiday_sw": {
        "dp_id": 165,
        "code": "holiday_sw",
        "name": "Holiday Mode",
        "icon": "mdi:beach",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# Number Types - read-write, scale 1 (tenths of a degree)
NUMBER_TYPES = {
    "cool_temp_set": {
        "dp_id": 102,
        "code": "cool_temp_set",
        "name": "Zone 1 Cooling Target Temperature",
        "icon": "mdi:thermometer-minus",
        "unit": "°C",
        "min_value": 7.0,
        "max_value": 25.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "heat_temp_set": {
        "dp_id": 103,
        "code": "heat_temp_set",
        "name": "Zone 1 Heating Target Temperature",
        "icon": "mdi:thermometer-plus",
        "unit": "°C",
        "min_value": 25.0,
        "max_value": 55.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "hot_water_temp_set": {
        "dp_id": 104,
        "code": "hot_water_temp_set",
        "name": "Hot Water Target Temperature",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 25.0,
        "max_value": 60.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "auto_temp_set": {
        "dp_id": 105,
        "code": "auto_temp_set",
        "name": "Zone 1 Auto Cooling Target Temperature",
        "icon": "mdi:thermometer-minus",
        "unit": "°C",
        "min_value": 7.0,
        "max_value": 25.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "auto_heat_temp_set_z1": {
        "dp_id": 158,
        "code": "auto_heat_temp_set_z1",
        "name": "Zone 1 Auto Heating Target Temperature",
        "icon": "mdi:thermometer-plus",
        "unit": "°C",
        "min_value": 25.0,
        "max_value": 55.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "cool_temp_set_z2": {
        "dp_id": 160,
        "code": "cool_temp_set_z2",
        "name": "Zone 2 Cooling Target Temperature",
        "icon": "mdi:thermometer-minus",
        "unit": "°C",
        "min_value": 7.0,
        "max_value": 25.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "heat_temp_set_z2": {
        "dp_id": 161,
        "code": "heat_temp_set_z2",
        "name": "Zone 2 Heating Target Temperature",
        "icon": "mdi:thermometer-plus",
        "unit": "°C",
        "min_value": 25.0,
        "max_value": 55.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "auto_cool_temp_set_z2": {
        "dp_id": 162,
        "code": "auto_cool_temp_set_z2",
        "name": "Zone 2 Auto Cooling Target Temperature",
        "icon": "mdi:thermometer-minus",
        "unit": "°C",
        "min_value": 7.0,
        "max_value": 25.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "auto_heat_temp_set_z2": {
        "dp_id": 163,
        "code": "auto_heat_temp_set_z2",
        "name": "Zone 2 Auto Heating Target Temperature",
        "icon": "mdi:thermometer-plus",
        "unit": "°C",
        "min_value": 25.0,
        "max_value": 55.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
    "idr_temp_set": {
        "dp_id": 164,
        "code": "idr_temp_set",
        "name": "Indoor Target Temperature",
        "icon": "mdi:home-thermometer",
        "unit": "°C",
        "min_value": 17.0,
        "max_value": 30.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10",
    },
}

# Select Types - read-write enums
SELECT_TYPES = {
    "work_mode": {
        "dp_id": 109,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:cog",
        "options": {
            "cool": "Cooling",
            "heat": "Heating",
            "auto": "Auto",
            "hot_water": "Hot Water",
            "cool_hot_water": "Cooling + Hot Water",
            "heat_hot_water": "Heating + Hot Water",
            "auto_dhw": "Auto + Hot Water",
        },
    },
    "zone_select": {
        # Meaning of the four values is not known yet. Reads 1 on the reported unit.
        "dp_id": 159,
        "code": "zone_select",
        "name": "Zone Selection",
        "icon": "mdi:view-dashboard-outline",
        "options": {
            "0": "Option 0",
            "1": "Option 1",
            "2": "Option 2",
            "3": "Option 3",
        },
    },
}
