# ====================================================
# TEC HS8/HS10 Monoblock (The Energy Combination) @akalverboer, issue #123
# Tuya modelId: 000002y2ml
# Air-to-water monobloc heat pump with heating, cooling and hot water.
# Temperatures, pressures and the water flow are sent with scale 1
# (306 = 30.6 degrees C, 40 = 4.0 bar, 14 = 1.4 m3/h).
#
# Names follow the meaning of the cloud schema, not its codes: for
# example "temp_current" is the return gas temperature, "temp_coiler"
# the evaporating pressure and "compressor_state" the boiler status.
#
# The fault data points only carry the unit's alarm codes (AL01 ...),
# without a description; the sensors show the active codes.
#
# The unit has no data point to choose the operating mode; the working
# state (dp 105) shows what it is doing.
#
# Not exposed on purpose:
#   - timer (dp 12): raw timer table.
# ====================================================
"""Model mapping for TEC HS8/HS10 Monoblock (000002y2ml)."""

MODEL_NAME = "TEC HS8/HS10 Monoblock (000002y2ml)"

# Sensor Types - read-only
SENSOR_TYPES = {
    "water_inlet_temp": {
        "dp_id": 22,
        "code": "temp_bottom",
        "name": "Water Inlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "water_outlet_temp": {
        "dp_id": 25,
        "code": "temp_effluent",
        "name": "Water Outlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "hot_water_temp": {
        "dp_id": 21,
        "code": "temp_top",
        "name": "Hot Water Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "ambient_temp": {
        "dp_id": 26,
        "code": "temp_around",
        "name": "Outdoor Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer-outline",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "room_temp": {
        # Room sensor of the unit; reads 0 when none is connected.
        "dp_id": 39,
        "code": "venting_temp_f",
        "name": "Room Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "discharge_temp": {
        "dp_id": 24,
        "code": "temp_venting",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-high",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "return_gas_temp": {
        "dp_id": 16,
        "code": "temp_current",
        "name": "Return Gas Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "evaporating_pressure": {
        "dp_id": 23,
        "code": "temp_coiler",
        "name": "Evaporating Pressure",
        "unit": "bar",
        "icon": "mdi:gauge-low",
        "device_class": "pressure",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "condensing_pressure": {
        "dp_id": 104,
        "code": "HPS",
        "name": "Condensing Pressure",
        "unit": "bar",
        "icon": "mdi:gauge-full",
        "device_class": "pressure",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "water_flow": {
        "dp_id": 107,
        "code": "flowrate",
        "name": "Water Flow",
        "unit": "m³/h",
        "icon": "mdi:water-pump",
        "device_class": "volume_flow_rate",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "compressor_freq": {
        "dp_id": 20,
        "code": "compressor_strength",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
    },
    "workstate": {
        # Read-only; also tells the thermostat card whether the unit heats.
        "dp_id": 105,
        "code": "workstate",
        "name": "Working State",
        "icon": "mdi:heat-pump",
        "conversion": "{'heating': 'Heating', 'cooling': 'Cooling', 'antifreeze': 'Antifreeze', 'defrosting': 'Defrosting', 'standby': 'Standby', 'off': 'Off', 'starting': 'Starting', 'on': 'On', 'domestic_hot_water': 'Hot Water'}.get(value, value)",
    },
    "fault_description": {
        # Bitmap; bit 0 = AL01 ... bit 29 = AL132 (order of the cloud schema).
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Codes",
        "icon": "mdi:alert-circle",
        "conversion": "', '.join(n for b, n in [(1,'AL01'),(2,'AL02'),(4,'AL03'),(8,'AL05'),(16,'AL17'),(32,'AL18'),(64,'AL19'),(128,'AL20'),(256,'AL21'),(512,'AL37'),(1024,'AL38'),(2048,'AL71'),(4096,'AL72'),(8192,'AL73'),(16384,'AL74'),(32768,'AL75'),(65536,'AL76'),(131072,'AL00'),(262144,'AL24'),(524288,'AL57'),(1048576,'AL78'),(2097152,'AL126'),(4194304,'AL127'),(8388608,'AL128'),(16777216,'AL129'),(33554432,'AL130'),(67108864,'AL107'),(134217728,'AL108'),(268435456,'AL131'),(536870912,'AL132')] if int(value) & b) or 'OK'",
    },
    "fault2": {
        "dp_id": 108,
        "code": "fault2",
        "name": "Fault Codes 2",
        "icon": "mdi:alert-circle-outline",
        "conversion": "'OK' if value == 'NONE' else value",
    },
}

# Binary Sensor Types - read-only
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault",
        "device_class": "problem",
        "conversion": "int(value) != 0",
    },
    "boiler_state": {
        # Called boiler status in the cloud schema despite its code.
        "dp_id": 27,
        "code": "compressor_state",
        "name": "Boiler",
        "icon": "mdi:water-boiler",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "secondary_pump": {
        "dp_id": 28,
        "code": "four_valve_state",
        "name": "Secondary Water Pump",
        "icon": "mdi:pump",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "water_pump": {
        "dp_id": 30,
        "code": "pump_state",
        "name": "Water Pump",
        "icon": "mdi:pump",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "heating_heater": {
        "dp_id": 32,
        "code": "ele_heating_state",
        "name": "Heating Electric Heater",
        "icon": "mdi:radiator",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "dhw_heater": {
        "dp_id": 109,
        "code": "DHW_heater",
        "name": "Hot Water Electric Heater",
        "icon": "mdi:water-boiler",
        "device_class": "running",
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
    "instant_heating": {
        "dp_id": 8,
        "code": "instant_heating",
        "name": "Hot Water",
        "icon": "mdi:water-boiler",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# Number Types - read-write values (scale 1, whole degrees)
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 4,
        "code": "temp_set",
        "name": "Heating Target Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 20.0,
        "max_value": 75.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "int(value * 10 + 0.5)",
    },
    "hotwatertemp": {
        "dp_id": 101,
        "code": "hotwatertemp",
        "name": "Hot Water Target Temperature",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 20.0,
        "max_value": 75.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "int(value * 10 + 0.5)",
    },
    "coolingtempsetup": {
        "dp_id": 102,
        "code": "coolingtempsetup",
        "name": "Cooling Target Temperature",
        "icon": "mdi:snowflake-thermometer",
        "unit": "°C",
        "min_value": 12.0,
        "max_value": 40.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "int(value * 10 + 0.5)",
    },
    "room_temp_set": {
        "dp_id": 34,
        "code": "temp_set_f",
        "name": "Room Target Temperature",
        "icon": "mdi:home-thermometer",
        "unit": "°C",
        "min_value": 10.0,
        "max_value": 30.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "int(value * 10 + 0.5)",
    },
}

# Thermostat card (optional, Options > thermostat): power, water outlet
# temperature and heating target; the working state tells heating from
# idle.
CLIMATE_HINTS = {
    "defaults": {
        "power": "switch",
        "current": "water_outlet_temp",
        "target": "temp_set",
    },
    "action": {
        "code": "workstate",
        "heating": ["heating", "domestic_hot_water"],
        "cooling": ["cooling"],
        "idle": ["standby", "off", "starting", "on", "antifreeze", "defrosting"],
    },
}
