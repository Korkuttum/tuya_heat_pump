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
BINARY_SENSOR_TYPES = {}

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
