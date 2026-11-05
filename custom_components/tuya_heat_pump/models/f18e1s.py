"""Adlar Fjord Pro - Tuya model f18e1s.

Validated against an Adlar Fjord Pro controller using:
- Tuya Cloud model data
- Direct TinyTuya local communication
- Physical Fjord controller display

Tuya protocol: 3.5

Known limitations:
- DP106 / Probe 2 is defined in Tuya but is not currently published.
- DP107 / Probe 3 is published but appears stale and does not track the
  physical controller reliably.
- DP108 / Probe 4 is defined but is not currently published.
"""

MODEL_NAME = "Adlar Fjord Pro"


# ============================================================
# SENSORS
# ============================================================

SENSOR_TYPES = {

    # --------------------------------------------------------
    # Temperature probes
    # --------------------------------------------------------

    # DP105
    # Validated against the physical controller.
    # Also confirmed to generate local push updates.
    "temp_1": {
        "dp_id": 105,
        "code": "temp_1",
        "name": "Water Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },

    # DP106
    # Defined by the Tuya model but not currently returned
    # by the Fjord's local Tuya interface.
    "temp_2": {
        "dp_id": 106,
        "code": "temp_2",
        "name": "Temperature Probe 2",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },

    # DP107
    # Present but currently stale/unreliable.
    "temp_3": {
        "dp_id": 107,
        "code": "temp_3",
        "name": "Temperature Probe 3",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },

    # DP108
    # Defined by the Tuya model but not currently returned.
    "temp_4": {
        "dp_id": 108,
        "code": "temp_4",
        "name": "Temperature Probe 4",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },

    # --------------------------------------------------------
    # Operating states
    # --------------------------------------------------------

    # DP114
    # Confirmed states include:
    # disabled
    # enabled
    # timer  = compressor start delay
    # active = compressor running
    # df     = defrost
    "comp": {
        "dp_id": 114,
        "code": "comp",
        "name": "Compressor Status",
        "icon": "mdi:heat-pump",
    },

    # DP115
    "res": {
        "dp_id": 115,
        "code": "res",
        "name": "Electric Heater Status",
        "icon": "mdi:heating-coil",
    },

    # DP165
    # Confirmed:
    # loading = fan starting/countdown
    # active  = fan running
    "vp_state": {
        "dp_id": 165,
        "code": "vp_state",
        "name": "Fan Status",
        "icon": "mdi:fan",
    },
    
    # --------------------------------------------------------
    # Energy consumption
    # --------------------------------------------------------

    # DP159
    # Tuya name: res_power
    # Tuya schema reports scale 3 and unit kWh.
    #
    # Represents electric-heater energy consumed during the
    # most recent 15-minute accounting interval.
    #
    # Raw values use scale 3:
    #   20  -> 0.020 kWh
    #   110 -> 0.110 kWh
    #
    # This is an interval/delta value, NOT a cumulative meter.
    # Use as a delta source when creating HA utility meters.
    "heater_interval_energy": {
        "dp_id": 159,
        "code": "res_power",
        "name": "Electric Heater 15 Minute Energy",
        "unit": "kWh",
        "icon": "mdi:lightning-bolt",
        "device_class": "energy",
        "state_class": "measurement",
        "conversion": "value / 1000",
    },

    # DP160
    # Tuya name: comp_power
    # Tuya schema reports scale 3 and unit kWh.
    #
    # Confirmed from local push monitoring to update at
    # approximately 15-minute boundaries.
    #
    # Observed sequence while compressor was operating:
    #   20  -> 0.020 kWh
    #   110 -> 0.110 kWh
    #   127 -> 0.127 kWh
    #   130 -> 0.130 kWh
    #   132 -> 0.132 kWh
    #
    # After the compressor stopped, the following complete
    # reporting interval returned 0.
    #
    # This is an interval/delta value, NOT a cumulative meter.
    # Use as a delta source when creating HA utility meters.
    "compressor_interval_energy": {
        "dp_id": 160,
        "code": "comp_power",
        "name": "Compressor 15 Minute Energy",
        "unit": "kWh",
        "icon": "mdi:lightning-bolt",
        "device_class": "energy",
        "state_class": "measurement",
        "conversion": "value / 1000",
    },

    # --------------------------------------------------------
    # Controller parameters
    # --------------------------------------------------------

    # DP117
    "h01": {
        "dp_id": 117,
        "code": "h01",
        "name": "Compressor Differential H01",
        "unit": "°C",
        "icon": "mdi:thermometer-lines",
    },

    # DP119
    "h02": {
        "dp_id": 119,
        "code": "h02",
        "name": "Electric Heater Differential H02",
        "unit": "°C",
        "icon": "mdi:thermometer-lines",
    },

    # --------------------------------------------------------
    # System status
    # --------------------------------------------------------

    # DP128
    "disinfect": {
        "dp_id": 128,
        "code": "disinfect",
        "name": "Disinfection Status",
        "icon": "mdi:bacteria-outline",
    },

    # DP155
    # Tuya gives this a misleading internal name, but its enum
    # contains the Fjord fault codes and ERR_NONE.
    "vwd3": {
        "dp_id": 155,
        "code": "vwd3",
        "name": "Fault Status",
        "icon": "mdi:alert-circle-outline",
    },
    
    
}


# ============================================================
# BINARY SENSORS
# ============================================================

BINARY_SENSOR_TYPES = {

    # DP111
    # Observed locally and tracks the compressor command state.
    "comp_cmd": {
        "dp_id": 111,
        "code": "comp_cmd",
        "name": "Compressor Enabled",
        "icon": "mdi:heat-pump",
        "conversion": (
            "value in [1, True, '1', 'true', 'on', "
            "'yes', 'enable', 'enabled']"
        ),
    },

    # DP112
    "res_cmd": {
        "dp_id": 112,
        "code": "res_cmd",
        "name": "Electric Heater Enabled",
        "icon": "mdi:heating-coil",
        "conversion": (
            "value in [1, True, '1', 'true', 'on', "
            "'yes', 'enable', 'enabled']"
        ),
    },

    # DP113
    "pv": {
        "dp_id": 113,
        "code": "pv",
        "name": "PV Input",
        "icon": "mdi:solar-power",
        "conversion": (
            "value in [1, True, '1', 'true', 'on', "
            "'yes', 'enable', 'enabled']"
        ),
    },

}


# ============================================================
# NUMBER CONTROLS
# ============================================================

NUMBER_TYPES = {

    # DP116 - P01 Compressor Setpoint
    #
    # Validated read/write using both TinyTuya and Home Assistant.
    # int(value) is IMPORTANT. HA supplies number values as floats.
    # Sending the float directly caused the physical Fjord display
    # to temporarily interpret 52 as 520.
    #
    # Manufacturer range: 10-60 °C.
    "p01": {
        "dp_id": 116,
        "code": "p01",
        "name": "Compressor Setpoint",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 10.0,
        "max_value": 60.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "int(value)",
    },

    # DP118 - P02 Electric Heater Setpoint
    #
    # Validated read/write through Home Assistant.
    # Manufacturer range: 10-65 °C.
    "p02": {
        "dp_id": 118,
        "code": "p02",
        "name": "Electric Heater Setpoint",
        "icon": "mdi:water-boiler",
        "unit": "°C",
        "min_value": 10.0,
        "max_value": 65.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "int(value)",
    },
}


# ============================================================
# SELECT CONTROLS
# ============================================================

SELECT_TYPES = {

    # DP5
    # Validated locally. Changes are pushed immediately by the Fjord.
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Operating Mode",
        "icon": "mdi:heat-pump-outline",
        "options": {
            "Eco": "Eco",
            "Auto": "Auto",
            "Boost": "Boost",
        },
    },
}


# ============================================================
# SWITCH CONTROLS
# ============================================================

# DP111, DP112, DP129 and other writable Tuya values are left out for
# now — not validated enough to expose as direct equipment commands.
#
# DP1 and DP126 are added below: both are declared accessMode "rw",
# type bool directly in Tuya's own cloud thing model (see issue #105),
# not just inferred from a raw reading.

SWITCH_TYPES = {

    # DP1
    # Main Fjord power switch.
    #
    # Tuya schema: read/write bool (Tuya name: "开关" / "switch").
    #
    # Use carefully in automations. Turning this off may stop normal
    # DHW recovery and potentially other controller functions.
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": (
            "value in [1, True, '1', 'true', 'on', "
            "'yes', 'enable', 'enabled', 'open']"
        ),
    },

    # DP126
    # Vacation mode. Previously exposed as a binary sensor only;
    # moved here since it's a validated read/write bool.
    "vstate": {
        "dp_id": 126,
        "code": "vstate",
        "name": "Vacation Mode",
        "icon": "mdi:beach",
        "conversion": (
            "value in [1, True, '1', 'true', 'on', "
            "'yes', 'enable', 'enabled']"
        ),
    },
}


# ============================================================
# TEXT CONTROLS
# ============================================================

TEXT_TYPES = {}