CAR_ISSUES = {
    "dent",
    "scratch",
    "crack",
    "glass_shatter",
    "broken_part",
    "missing_part",
    "none",
    "unknown",
}


CAR_OBJECT_PARTS = {
    "front_bumper",
    "rear_bumper",
    "door",
    "hood",
    "windshield",
    "side_mirror",
    "headlight",
    "taillight",
    "fender",
    "quarter_panel",
    "body",
    "unknown",
}


ISSUE_TO_REQUIREMENT = {
    "dent": "REQ_CAR_BODY_PANEL",
    "scratch": "REQ_CAR_BODY_PANEL",

    "crack": "REQ_CAR_GLASS_LIGHT_MIRROR",
    "glass_shatter": "REQ_CAR_GLASS_LIGHT_MIRROR",
    "broken_part": "REQ_CAR_GLASS_LIGHT_MIRROR",
    "missing_part": "REQ_CAR_GLASS_LIGHT_MIRROR",
}