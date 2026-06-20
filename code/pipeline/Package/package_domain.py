PACKAGE_ISSUES = {
    "torn_packaging",
    "crushed_packaging",
    "water_damage",
    "stain",
    "missing_part",
    "none",
    "unknown",
}

PACKAGE_OBJECT_PARTS = {
    "box",
    "package_corner",
    "package_side",
    "seal",
    "label",
    "contents",
    "item",
    "unknown",
}

ISSUE_TO_REQUIREMENT = {

    "torn_packaging":
        "REQ_PACKAGE_TORN",

    "crushed_packaging":
        "REQ_PACKAGE_CRUSHED",

    "water_damage":
        "REQ_PACKAGE_WATER",

    "stain":
        "REQ_PACKAGE_WATER",

    "missing_part":
        "REQ_PACKAGE_CONTENTS",
}