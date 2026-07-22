"""Model mapping for Coffee Machine (modelId: ew8plw)."""

MODEL_NAME = "Coffee Machine (ew8plw)"
# ====================================================
# Coffee Machine @Korkuttum
# modelId: ew8plw
# DP map sourced from /v2.0/cloud/thing/{id}/shadow/properties + /model
# Notes:
#   - profileorange/violet/blue/green (dp 101-104) are raw 128-byte
#     per-profile settings blobs. Internal field layout not decoded yet —
#     left unmapped until run through raw_explorer.py.
#   - favor (dp 112) is a raw per-profile favorites blob, also undecoded.
#   - orange/violet/blue/green_username (dp 108-111) ARE decoded: each is
#     the whole raw DP read as a UTF-8 string (profile display name),
#     contributed via raw_explorer.py's "text" field type — see the
#     TEXT_TYPES block at the bottom of this file.
#   - work_state (dp 3) and fault (dp 4) are read-only (accessMode "ro").
#   - Everything else here is accessMode "rw".
# ====================================================

SENSOR_TYPES = {
    "work_state": {
        "dp_id": 3,
        "code": "work_state",
        "name": "Work State",
        "icon": "mdi:coffee-maker",
    },
    # Fault Description (dp_id: 4) — Tuya's label array for this DP is
    # already in English (unusual, most devices need Chinese
    # translation), so used as-is, just cleaned up for readability.
    # 11-bit bitmap, decodes into readable fault name(s), lists all
    # active faults if more than one bit is set at once.
    "fault": {
        "dp_id": 4,
        "code": "fault",
        "name": "Fault Description",
        "icon": "mdi:alert-circle",
        "conversion": (
            "', '.join(n for b, n in ["
            "(1,'Heating Fault'),"
            "(2,'NTC Sensor Fault'),"
            "(4,'Blocked'),"
            "(8,'Front Door Open'),"
            "(16,'Brew Unit Misplaced'),"
            "(32,'Water Empty'),"
            "(64,'Trash Can Misplaced'),"
            "(128,'Bean Container Empty'),"
            "(256,'Residual Container Full'),"
            "(512,'Milk Cup Missing'),"
            "(1024,'Water Tank Misplaced')"
            "] if value & b) or 'OK'"
        ),
    },
}

BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 4,
        "code": "fault",
        "name": "Fault Alarm",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    # Per-bit fault binary sensors — all share the same "fault" DP
    # (dp_id 4) via an explicit "code" override, each checking one bit
    # with its own mask. Added alongside the readable multi-fault
    # SENSOR_TYPES entry above so both approaches can be compared in
    # practice — keep whichever turns out more useful, or both.
    "fault_heating_fault": {
        "dp_id": 4,
        "code": "fault",
        "name": "Heating Fault",
        "device_class": "problem",
        "conversion": "bool(value & 1)",
    },
    "fault_ntc_fault": {
        "dp_id": 4,
        "code": "fault",
        "name": "NTC Sensor Fault",
        "device_class": "problem",
        "conversion": "bool(value & 2)",
    },
    "fault_blocking": {
        "dp_id": 4,
        "code": "fault",
        "name": "Blocked",
        "device_class": "problem",
        "conversion": "bool(value & 4)",
    },
    "fault_frontdoor_open": {
        "dp_id": 4,
        "code": "fault",
        "name": "Front Door Open",
        "device_class": "problem",
        "conversion": "bool(value & 8)",
    },
    "fault_bu_misplaced": {
        "dp_id": 4,
        "code": "fault",
        "name": "Brew Unit Misplaced",
        "device_class": "problem",
        "conversion": "bool(value & 16)",
    },
    "fault_water_empty": {
        "dp_id": 4,
        "code": "fault",
        "name": "Water Empty",
        "device_class": "problem",
        "conversion": "bool(value & 32)",
    },
    "fault_trashcan_misplaced": {
        "dp_id": 4,
        "code": "fault",
        "name": "Trash Can Misplaced",
        "device_class": "problem",
        "conversion": "bool(value & 64)",
    },
    "fault_beancontainer_empty": {
        "dp_id": 4,
        "code": "fault",
        "name": "Bean Container Empty",
        "device_class": "problem",
        "conversion": "bool(value & 128)",
    },
    "fault_residual_full": {
        "dp_id": 4,
        "code": "fault",
        "name": "Residual Container Full",
        "device_class": "problem",
        "conversion": "bool(value & 256)",
    },
    "fault_milkcup_missing": {
        "dp_id": 4,
        "code": "fault",
        "name": "Milk Cup Missing",
        "device_class": "problem",
        "conversion": "bool(value & 512)",
    },
    "fault_watertank_misplaced": {
        "dp_id": 4,
        "code": "fault",
        "name": "Water Tank Misplaced",
        "device_class": "problem",
        "conversion": "bool(value & 1024)",
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
    "start": {
        "dp_id": 2,
        "code": "start",
        "name": "Start",
        "icon": "mdi:coffee",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "auto_clean": {
        "dp_id": 13,
        "code": "auto_clean",
        "name": "Auto Clean",
        "icon": "mdi:dishwasher",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "descaling": {
        "dp_id": 14,
        "code": "descaling",
        "name": "Descaling",
        "icon": "mdi:water-alert",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "factory_reset": {
        "dp_id": 17,
        "code": "factory_reset",
        "name": "Factory Reset",
        "icon": "mdi:restore",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "empty_device": {
        "dp_id": 23,
        "code": "empty_device",
        "name": "Empty Device",
        "icon": "mdi:cup-off",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "double": {
        "dp_id": 114,
        "code": "double",
        "name": "Double Cup",
        "icon": "mdi:cup",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "rinsing_clean": {
        "dp_id": 115,
        "code": "rinsing_clean",
        "name": "Rinsing Clean",
        "icon": "mdi:water-sync",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "milk_cupclean": {
        "dp_id": 116,
        "code": "milk_cupclean",
        "name": "Milk Cup Clean",
        "icon": "mdi:cup-water",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "hotwaterdispensing": {
        "dp_id": 117,
        "code": "hotwaterdispensing",
        "name": "Hot Water Dispensing",
        "icon": "mdi:kettle-steam",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "espressoshot": {
        "dp_id": 118,
        "code": "espressoshot",
        "name": "Espresso Shot",
        "icon": "mdi:coffee",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "milkfrothing": {
        "dp_id": 119,
        "code": "milkfrothing",
        "name": "Milk Frothing",
        "icon": "mdi:coffee-outline",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "pre_brew": {
        "dp_id": 120,
        "code": "pre_brew",
        "name": "Pre-Brew",
        "icon": "mdi:coffee-to-go",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

NUMBER_TYPES = {
    "water_hardness": {
        "dp_id": 107,
        "code": "water_hardness",
        "name": "Water Hardness",
        "icon": "mdi:water-percent",
        "min_value": 1.0,
        "max_value": 5.0,
        "step": 1.0,
    },
}

SELECT_TYPES = {
    "drink_set": {
        "dp_id": 6,
        "code": "drink_set",
        "name": "Drink Selection",
        "icon": "mdi:coffee",
        "options": {
            "Espresso": "Espresso",
            "Americano": "Americano",
            "Lungo": "Lungo",
            "CaffeLatte": "Caffe Latte",
            "LatteMacchiato": "Latte Macchiato",
            "Ristretto": "Ristretto",
            "Doppio": "Doppio",
            "EspressoMacchiato": "Espresso Macchiato",
            "RistrettoBianco": "Ristretto Bianco",
            "FlatWhite": "Flat White",
            "Cortado": "Cortado",
            "IcedAmericano": "Iced Americano",
            "IcedLatte": "Iced Latte",
            "Hotwater": "Hot Water",
            "Hotmilk": "Hot Milk",
            "TravelMug": "Travel Mug",
            "Cappuccino": "Cappuccino",
        },
    },
    "aso_timer": {
        "dp_id": 105,
        "code": "aso_timer",
        "name": "Auto Shutoff Timer",
        "icon": "mdi:timer-outline",
        "options": {
            "10Minutes": "10 Minutes",
            "20Minutes": "20 Minutes",
            "30Minutes": "30 Minutes",
            "1hour": "1 Hour",
            "2hours": "2 Hours",
            "3hours": "3 Hours",
            "6hours": "6 Hours",
            "12hours": "12 Hours",
            "24hours": "24 Hours",
        },
    },
    "mode_selection": {
        "dp_id": 106,
        "code": "mode_selection",
        "name": "Mode",
        "icon": "mdi:leaf",
        "options": {
            "Default": "Default",
            "ECO": "Eco",
        },
    },
    "last_profile": {
        "dp_id": 113,
        "code": "last_profile",
        "name": "Active Profile",
        "icon": "mdi:account",
        "options": {
            "guest": "Guest",
            "orange": "Orange",
            "violet": "Violet",
            "blue": "Blue",
            "green": "Green",
        },
    },
}

# --- merge into TEXT_TYPES (from raw_explorer.py, unchanged) ---
TEXT_TYPES = globals().get("TEXT_TYPES", {})
TEXT_TYPES.update({
    "orange_username": {
        "dp_id": 108,
        "code": "orange_username",
        "raw_source": "orange_username",
        "field_index": 0,
        "encoding": "utf8_string",
        "max_length": 16,
        "name": "Orange Username",
    },
    "violet_username": {
        "dp_id": 109,
        "code": "violet_username",
        "raw_source": "violet_username",
        "field_index": 0,
        "encoding": "utf8_string",
        "max_length": 16,
        "name": "Violet Username",
    },
    "blue_username": {
        "dp_id": 110,
        "code": "blue_username",
        "raw_source": "blue_username",
        "field_index": 0,
        "encoding": "utf8_string",
        "max_length": 16,
        "name": "Blue Username",
    },
    "green_username": {
        "dp_id": 111,
        "code": "green_username",
        "raw_source": "green_username",
        "field_index": 0,
        "encoding": "utf8_string",
        "max_length": 16,
        "name": "Green Username",
    },
})
