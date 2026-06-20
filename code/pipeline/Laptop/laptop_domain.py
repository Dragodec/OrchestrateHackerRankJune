LAPTOP_ISSUES = {
    "dent",
    "scratch",
    "crack",
    "glass_shatter",
    "broken_part",
    "missing_part",
    "stain",
    "water_damage",
    "none",
    "unknown",
}


LAPTOP_OBJECT_PARTS = {
    "screen",
    "keyboard",
    "trackpad",
    "hinge",
    "lid",
    "corner",
    "port",
    "base",
    "body",
    "unknown",
}


ISSUE_TO_REQUIREMENT = {

    # Screen related
    "crack": "REQ_LAPTOP_SCREEN",
    "glass_shatter": "REQ_LAPTOP_SCREEN",

    # Physical hardware damage
    "dent": "REQ_LAPTOP_BODY",
    "scratch": "REQ_LAPTOP_BODY",
    "broken_part": "REQ_LAPTOP_HARDWARE",
    "missing_part": "REQ_LAPTOP_HARDWARE",

    # Liquid / staining
    "water_damage": "REQ_LAPTOP_LIQUID_DAMAGE",
    "stain": "REQ_LAPTOP_LIQUID_DAMAGE",
}