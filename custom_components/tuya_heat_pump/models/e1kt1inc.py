"""Model mapping for Swim&Fun Fjord / Zile HF006A "Inverboost" pool heat pump (modelId: e1kt1inc).

Product: "Inverboost"  |  product_id: svwcisuc1wqcmjth  |  OEM: 佛山资乐 (Foshan Zile) HF006A
Rebadged as Swim&Fun Fjord 1447 (11 kW) and other Fairland-family inverter pool pumps.
Manufacturer range (other Fjord heat-pump models):
  https://www.swim-fun.com/sortiment/pool-and-spa-bath-heating/heat-pumps

This unit exposes almost all engineering telemetry ONLY inside two base64 `raw` DPs:
  - dp 135 (code "r_135"): system + refrigeration-circuit temps, EEV, fan, inverter output V/A/temp
  - dp 136 (code "r_136"): inverter status, mains + inverter electrical, compressor frequency, module temps
Both are int16 big-endian arrays (2-byte fields). Field offsets below were reverse-engineered
and verified slot-by-slot against the vendor app's "Status Overview" while the compressor was
running (2026-07-11): slow values matched to the decimal, electrical within ~2 %, fast
refrigeration temps within cloud-shadow lag.

Idle behaviour: unused/refrigeration slots report the sentinel -32700 when the compressor is off,
so those conversions null the sentinel out (`None if value == -32700 else ...`).
"""

MODEL_NAME = "Swim&Fun Fjord / Zile HF006A Inverboost Pool Heat Pump (e1kt1inc)"

# ACTIVE-FAULT REGISTER `err_cur_id_info` (dp 107)
#
# A 244-byte raw block carried in the same cloud shadow as r_135/r_136, so
# reading it costs no extra API call. All-zero means no active fault.
#
# Encoding, confirmed against two deliberately provoked x072 faults (water
# flow stopped while the unit was running):
#
#     00 FF 00 48 00 00 ...   ->  int16_be slot 0 = 255, slot 1 = 72
#     |__ module |__ code
#
# A value list, not a bitmap: read as bits, the observed frame would imply
# x008/x009/x010 active, which are not defined codes. Slot 0 is the module
# id in the manual's own notation -- page 345 defines it as "FF = System,
# 00 = Module board no. 0", and the parameter table is scoped "FF (System)"
# and "00~08 (Module)".
#
# Two consequences for any model with a similar register:
#
# - "A fault is present" must be tested on the module slot, or on the whole
#   register being non-zero -- NOT on the code slot. x000 is a real code, so
#   code == 0 does not mean "no fault". Corner case: board 0 is a valid
#   module id, so a fault raised by board 0 cannot be told from a clear
#   register on that slot alone. It cannot arise on this single-compressor
#   unit, which only ever reports 0xFF, and `fault_active` tests the whole
#   register.
#
# - The register BLINKS at every polling rate tested, so a consumer must
#   latch or debounce. Sampling the shadow directly every 20-30s returned 2
#   all-zero frames out of 8 polls; the integration's own 3-minute interval
#   returned 1 out of ~12, one poll wide. During the latter the unit's panel
#   still displayed the fault and every other sensor agreed it was live, so
#   the cloud shadow was briefly wrong, not the device.
#
# The manual never defines the literal "x" prefix -- the error table prints
# x000..x140 with no legend. The NUMBER is the identity; "x072" reproduces
# the manual's notation without interpreting it.
#
# The unit's panel can look like evidence against the module slot and is
# not: during a provoked x072 it read "0072" while the module slot read
# 255. Page 337 explains it -- an active fault is shown in the display's
# clock area, a four-digit HH:MM field, so "0072" is the code zero-padded
# by display geometry and carries no module information.
#
# Open question: with two simultaneous faults (page 337 says the panel then
# alternates between codes), is the layout repeating (module, code) records
# or one module marker followed by several codes? One fault cannot tell.
#
# `err_his_cmd` (dp 116) holds fault HISTORY but is a command channel
# (value None until written) with an unknown wire format.
#
# Codes below are the manual's English error table (pages 370-379), two
# families: H0xx main control board (H006 is not defined) and x0xx unit /
# inverter. Numbering is sparse. Names are the manual's own, normalized:
#   - it mixes "-" and an en dash as a pseudo-colon ("Discharge temperature
#     - sensor error"); dropped, since most entries already read "Fin sensor
#     error" without it
#   - "Interrupt Overflow 1" / "Task2 Overflow error" were title-cased
#     mid-string where every other entry is sentence case
#   - x065, x080 and x117 all read "Communication error"; the subsystem from
#     each row's own Causes column is appended so the code is actionable
# Cross-family duplicates are left alone: H004/x074, H005/x071 and H007/x067
# share a name but the prefix tells them apart.
# The manual documents x029 ("model setup in progress") and x075 ("anti-ice
# temperature too low", whose troubleshooting column reads "normal frost
# protection") as operating states rather than faults, yet the device still
# writes them to this register. Whether to act on them is a consumer
# decision, not something this model file makes.
ERROR_CODES = {
    'H001': 'Phase error protection',
    'H002': 'EEPROM data error (main unit)',
    'H003': 'Ambient temperature sensor error',
    'H004': 'Inlet temperature sensor error',
    'H005': 'Outlet temperature sensor error',
    'H007': 'Phase loss protection',
    'x000': 'Low compressor pressure',
    'x001': 'High compressor pressure',
    'x004': 'Fin sensor error',
    'x005': 'Discharge temperature sensor error',
    'x006': 'Discharge temperature too high',
    'x011': 'Suction temperature sensor error',
    'x012': 'Post-valve temperature error',
    'x013': 'Suction temperature too low',
    'x014': 'Frequent emergency defrosting',
    'x015': 'Abnormal difference between suction and discharge temperature',
    'x016': 'Evaporation temperature of refrigerant too low',
    'x019': 'Inlet water temperature too low',
    'x020': 'Inlet water temperature too high',
    'x021': 'Fan 1 abnormal speed',
    'x022': 'Fan 2 abnormal speed',
    'x027': 'Inverter communication error',
    'x028': 'Inverter error',
    'x029': 'Inverter model setup in progress',
    'x064': 'Module ambient temperature error',
    'x065': 'Communication error (wired controller)',
    'x066': 'EEPROM data error',
    'x067': 'Phase loss protection',
    'x069': 'Outlet temperature too low',
    'x070': 'Outlet temperature too high',
    'x071': 'Outlet temperature sensor error',
    'x072': 'Insufficient water flow',
    'x074': 'Inlet temperature sensor error',
    'x075': 'Anti-ice temperature too low',
    'x077': 'Large difference between outlet and inlet temperature',
    'x078': 'Irregular difference between outlet and inlet temperature',
    'x079': 'Power supply error',
    'x080': 'Communication error (control panel)',
    'x096': 'Overcurrent at startup',
    'x097': 'Overcurrent during acceleration',
    'x098': 'Overcurrent during deceleration',
    'x099': 'Overcurrent at constant speed',
    'x100': 'Overvoltage during acceleration',
    'x101': 'Overvoltage during deceleration',
    'x102': 'Overvoltage at constant speed',
    'x103': 'Overvoltage in standby',
    'x104': 'Undervoltage during operation',
    'x105': 'Input phase failure (three-phase only)',
    'x106': 'Output phase failure',
    'x107': 'Power unit protection',
    'x108': 'Inverter overheating',
    'x109': 'Inverter overload (PFC overheating)',
    'x110': 'Motor overload',
    'x111': 'PFC start error',
    'x112': 'Motor overload (load too high)',
    'x113': 'Motor overspeed',
    'x114': 'Motor D-axis overcurrent',
    'x115': 'Motor Q-axis overcurrent',
    'x116': 'Parameter storage failed',
    'x117': 'Communication error (inverter driver board)',
    'x118': 'Current test error',
    'x119': 'PFC temperature test error',
    'x120': 'Motor locked at startup',
    'x121': 'Motor locked during operation',
    'x122': 'Temperature test error',
    'x123': 'Stop error',
    'x124': 'Interrupt overflow 1',
    'x125': 'Interrupt overflow 2',
    'x126': 'Rotor stall at startup',
    'x127': 'Rotor stall during operation',
    'x128': 'PFC overcurrent',
    'x129': 'PFC peak current too high',
    'x130': 'PFC RMS current too high',
    'x131': 'Input phase reversed',
    'x132': 'Input frequency too high',
    'x133': 'Input frequency too low',
    'x134': 'Overvoltage at input',
    'x135': 'Undervoltage at input',
    'x136': 'Input phase voltage distortion',
    'x137': 'Overvoltage at output',
    'x138': 'Error in charging circuit',
    'x139': 'Task 2 overflow error',
    'x140': 'Task 2 operation error',
}

# The register carries the code as a plain number. These are the two
# lookups the sensors use, so no consumer needs its own copy of the table:
# one turns the number into the manufacturer's description, the other into
# the identifier the manual's table is keyed on.
FAULT_CODE_DESCRIPTIONS = {
    int(code[1:]): name
    for code, name in ERROR_CODES.items()
    if code.startswith("x")
}

# Module identifiers, verbatim from the manual's analog-measurement screen
# (page 345): "FF = System, 00 = Module board no. 0", with the parameter
# table on the next page scoped "FF (System)" and "00~08 (Module)". So the
# register's module slot is the same identifier the unit's own display
# shows, and 0xFF is the whole system rather than a numbered board.
# A single-compressor unit like this one only ever reports 255; the 0-8
# range exists for the multi-module members of the same controller family.
FAULT_MODULES = {255: "System"}
FAULT_MODULES.update({n: f"Module board {n}" for n in range(9)})

# ====================================================
# SENSOR TYPES (read-only)
# ====================================================
SENSOR_TYPES = {
    # ---- System water / ambient temps (r_135, always valid) ----
    "inlet_water_temperature": {
        "dp_id": 135,
        "code": "inlet_water_temperature",
        "raw_source": "r_135",
        "field_index": 0,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "outlet_water_temperature": {
        "dp_id": 135,
        "code": "outlet_water_temperature",
        "raw_source": "r_135",
        "field_index": 1,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "Outlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ambient_temperature": {
        "dp_id": 135,
        "code": "ambient_temperature",
        "raw_source": "r_135",
        "field_index": 2,
        "encoding": "int16_be",
        "conversion": "value / 10",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # ---- Refrigeration circuit (r_135, sentinel when idle) ----
    "coil_temperature": {
        "dp_id": 135,
        "code": "coil_temperature",
        "raw_source": "r_135",
        "field_index": 99,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "Coil Temperature",
        "unit": "°C",
        "icon": "mdi:heat-wave",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "exhaust_temperature": {
        "dp_id": 135,
        "code": "exhaust_temperature",
        "raw_source": "r_135",
        "field_index": 100,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "Discharge (Exhaust) Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-high",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "suction_temperature": {
        "dp_id": 135,
        "code": "suction_temperature",
        "raw_source": "r_135",
        "field_index": 101,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "Suction Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "valve_out_temperature": {
        "dp_id": 135,
        "code": "valve_out_temperature",
        "raw_source": "r_135",
        "field_index": 102,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "Valve Outlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "eev_pv_temperature": {
        "dp_id": 135,
        "code": "eev_pv_temperature",
        "raw_source": "r_135",
        "field_index": 109,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "EEV PV Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "eev_sv_temperature": {
        "dp_id": 135,
        "code": "eev_sv_temperature",
        "raw_source": "r_135",
        "field_index": 108,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "EEV SV Temperature",
        "unit": "°C",
        "icon": "mdi:valve-open",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "no_frost_ewd_temperature": {
        "dp_id": 135,
        "code": "no_frost_ewd_temperature",
        "raw_source": "r_135",
        "field_index": 114,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "No-Frost EWD Temperature",
        "unit": "°C",
        "icon": "mdi:snowflake-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "eev_step": {
        "dp_id": 135,
        "code": "eev_step",
        "raw_source": "r_135",
        "field_index": 97,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value",
        "name": "EEV Opening Step",
        "unit": "step",
        "icon": "mdi:valve",
        "state_class": "measurement",
    },
    "fan_target_speed": {
        "dp_id": 135,
        "code": "fan_target_speed",
        "raw_source": "r_135",
        "field_index": 115,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value",
        "name": "Fan Target Speed",
        "unit": "rpm",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    "fan_actual_speed": {
        "dp_id": 135,
        "code": "fan_actual_speed",
        "raw_source": "r_135",
        "field_index": 116,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value",
        "name": "Fan Actual Speed",
        "unit": "rpm",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    # ---- Inverter output to compressor (r_135, sentinel when idle) ----
    "inverter_output_voltage": {
        "dp_id": 135,
        "code": "inverter_output_voltage",
        "raw_source": "r_135",
        "field_index": 117,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "Inverter Output Voltage",
        "unit": "V",
        "icon": "mdi:sine-wave",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "inverter_output_current": {
        "dp_id": 135,
        "code": "inverter_output_current",
        "raw_source": "r_135",
        "field_index": 118,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "Inverter Output Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
    },
    "inverter_module_temperature": {
        "dp_id": 135,
        "code": "inverter_module_temperature",
        "raw_source": "r_135",
        "field_index": 119,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "Inverter Module Temperature",
        "unit": "°C",
        "icon": "mdi:chip",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # ---- Inverter status + electrical + frequency (r_136) ----
    "inverter_info": {
        "dp_id": 136,
        "code": "inverter_info",
        "raw_source": "r_136",
        "field_index": 0,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value",
        "name": "Inverter Info",
        "icon": "mdi:information-outline",
        "state_class": "measurement",
    },
    "mains_input_current": {
        "dp_id": 136,
        "code": "mains_input_current",
        "raw_source": "r_136",
        "field_index": 1,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "Mains Input Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
    },
    "inverter_output_power": {
        "dp_id": 136,
        "code": "inverter_output_power",
        "raw_source": "r_136",
        "field_index": 2,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 100",
        "name": "Inverter Output Power",
        "unit": "kW",
        "icon": "mdi:flash-outline",
        "device_class": "power",
        "state_class": "measurement",
    },
    "compressor_frequency_target": {
        "dp_id": 136,
        "code": "compressor_frequency_target",
        "raw_source": "r_136",
        "field_index": 3,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "Compressor Frequency Target",
        "unit": "rps",
        "icon": "mdi:sine-wave",
        "state_class": "measurement",
    },
    "compressor_frequency": {
        "dp_id": 136,
        "code": "compressor_frequency",
        "raw_source": "r_136",
        "field_index": 4,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "Compressor Frequency",
        "unit": "rps",
        "icon": "mdi:sine-wave",
        "state_class": "measurement",
    },
    "mains_input_voltage": {
        "dp_id": 136,
        "code": "mains_input_voltage",
        "raw_source": "r_136",
        "field_index": 16,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "Mains Input Voltage",
        "unit": "V",
        "icon": "mdi:sine-wave",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    # Module temps (r_136[40-42]) mirror the system temps; exposed for completeness.
    "module_inlet_temperature": {
        "dp_id": 136,
        "code": "module_inlet_temperature",
        "raw_source": "r_136",
        "field_index": 40,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "Module Inlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "entity_registry_enabled_default": False,
    },
    "module_outlet_temperature": {
        "dp_id": 136,
        "code": "module_outlet_temperature",
        "raw_source": "r_136",
        "field_index": 41,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "Module Outlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "entity_registry_enabled_default": False,
    },
    "module_ambient_temperature": {
        "dp_id": 136,
        "code": "module_ambient_temperature",
        "raw_source": "r_136",
        "field_index": 42,
        "encoding": "int16_be",
        "conversion": "None if value == -32700 else value / 10",
        "name": "Module Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "entity_registry_enabled_default": False,
    },
    # ---- Categorized water temperature (dp 24, non-raw) ----
    # NOTE: categorized dp 123 "inlet_temp" reads the -32700 sentinel (no external probe fitted) —
    # use the r_135[0] inlet sensor above instead; dp 123 is intentionally omitted.
    "water_temperature": {
        "dp_id": 24,
        "code": "water_temperature",
        "conversion": "None if value == -32700 else value / 10",
        "name": "Water Temperature",
        "unit": "°C",
        "icon": "mdi:pool-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "fault_description": {
        "dp_id": 107,
        "code": "fault_description",
        "raw_source": "err_cur_id_info",
        "field_index": 1,
        "guard_field_index": 0,
        "encoding": "int16_be",
        "value_map": FAULT_CODE_DESCRIPTIONS,
        "value_map_default": "Unknown fault code",
        "guard_inactive_value": "OK",
        "name": "Fault",
        "icon": "mdi:alert-circle-outline",
    },
    # Guarded on its own slot: a zero module slot means the register is
    # clear, and reporting that as "Module board 0" would be a real reading
    # of a value that is not one. See the note above on the corner case.
    "fault_module": {
        "dp_id": 107,
        "code": "fault_module",
        "raw_source": "err_cur_id_info",
        "field_index": 0,
        "guard_field_index": 0,
        "encoding": "int16_be",
        "value_map": FAULT_MODULES,
        "value_map_default": "Unknown module",
        "guard_inactive_value": "OK",
        "name": "Fault Module",
        "icon": "mdi:chip",
        "entity_category": "diagnostic",
    },
    # Formatted as a string on purpose, for two reasons. It renders the
    # identifier the manual's error table is keyed on ("x072"), which is
    # where a user looks up cause and troubleshooting. And it sidesteps the
    # float() at the end of the raw-field branch: a code is an identifier,
    # not a measurement, so it carries no state_class -- which means the
    # frontend prints the state verbatim rather than localizing it, and a
    # numeric value would show up as "72.0" with an unlocalized separator.
    # A conversion, rather than a value_map, so a code the table does not
    # list -- the numbering is sparse and stops at x140 -- still renders
    # its own number instead of collapsing to a default.
    "fault_code": {
        "dp_id": 107,
        "code": "fault_code",
        "raw_source": "err_cur_id_info",
        "field_index": 1,
        "guard_field_index": 0,
        "encoding": "int16_be",
        "conversion": "'x%03d' % value",
        "guard_inactive_value": "OK",
        "name": "Fault Code",
        "icon": "mdi:alert-circle-outline",
        "entity_category": "diagnostic",
    },
}

# ====================================================
# SWITCH TYPES (read-write bool)
# ====================================================
SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes']",
    },
}

# ====================================================
# NUMBER TYPES (read-write value)
# ====================================================
NUMBER_TYPES = {
    # Active-mode target setpoint (dp 16, °C, no scaling).
    "temp_set": {
        "dp_id": 16,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 10.0,
        "max_value": 85.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Secondary setpoint (dp 124) — per-mode target (verify which mode it follows).
    "temp_set_secondary": {
        "dp_id": 124,
        "code": "temp_set_1",
        "name": "Secondary Setpoint",
        "icon": "mdi:thermostat-box",
        "unit": "°C",
        "min_value": -10.0,
        "max_value": 85.0,
        "step": 1.0,
        "api_conversion": "value",
        "entity_registry_enabled_default": False,
    },
}

# ====================================================
# SELECT TYPES (read-write enum)
# ====================================================
SELECT_TYPES = {
    # Operating mode (dp 2). The device /model declares six enum values
    # (auto/cold/hot/dhw/cold_dhw/hot_dhw), but the dhw* variants are inherited
    # from generic heat-pump firmware and are NOT applicable to this pool unit
    # (no domestic-hot-water tank) — the device silently rejects them (dp 2 stays
    # on the prior mode). Only the physically valid modes are offered here.
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Operating Mode",
        "icon": "mdi:hvac",
        "options": {
            "auto": "Auto",
            "cold": "Cooling",
            "hot": "Heating",
        },
    },
}

# ====================================================
# BINARY SENSOR TYPES
# ====================================================
BINARY_SENSOR_TYPES = {
    # Encoding-agnostic presence check: base64 of an all-zero block
    # contains only 'A' plus '=' padding, so any other character means at
    # least one bit is set somewhere. Independent of the slot layout, which
    # keeps it valid for sibling models laid out differently -- and it is
    # the authority for "is a fault present", per the module-slot corner
    # case noted at the top of this file.
    "fault_active": {
        "dp_id": 107,
        "code": "err_cur_id_info",
        "name": "Fault Active",
        "device_class": "problem",
        "conversion": "value.strip('A=') != ''",
    },
}

# ====================================================
# WEEKLY SCHEDULE / TIMERS  (documented for future work)
# ====================================================
# Unlike some Tuya heat pumps (e.g. model eu20ns, whose weekly schedule lives in
# raw DPs 110-116 and is executed on-device), THIS firmware has NO schedule/timer
# data point at all — the device /model declares none, and decoding every raw
# array (r_135-150, r_171) with two active app schedules showed no time signature.
# Schedules are stored CLOUD-SIDE in Tuya's timer service; the cloud pushes the
# switch command over MQTT at the scheduled time.
#
# Reading the cloud schedule (read-only; not currently surfaced as an entity):
#   GET /v1.0/devices/{device_id}/timers?category=
#   The shadow-properties wrapper does NOT sign query strings, so sign manually:
#     string_to_sign = "GET\n" + sha256("") + "\n\n" + path
#     sign           = HMAC-SHA256(access_id + access_token + t + string_to_sign)
# Timer fields:
#   time         "HH:MM"
#   functions[]  {code:"switch", value:true/false}
#   loops        7-char weekday bitmap, SUNDAY-FIRST [Sun,Mon,Tue,Wed,Thu,Fri,Sat]
#                e.g. "1100101" = Sun+Mon+Thu+Sat ; "0000000" = one-shot
#   date         "YYYYMMDD" for a one-shot (else "00000000" for a repeating timer)
#   alias_name   free-text note
#   is_app_push  Tuya-app push notification flag (NOT surfaced to Home Assistant)
# Firing accuracy is ~±30 s.
