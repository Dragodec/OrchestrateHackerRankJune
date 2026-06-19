from models.parsed_claim import ParsedClaim


ISSUE_KEYWORDS = {
    "dent": [
        "dent",
        "dented",
    ],

    "scratch": [
        "scratch",
        "scratched",
    ],

    "crack": [
        "crack",
        "cracked",
    ],

    "glass_shatter": [
        "glass shattered",
        "shattered glass",
        "shattered windshield",
    ],

    "broken_part": [
        "broken",
        "damaged",
    ],

    "missing_part": [
        "missing",
        "fell off",
        "lost",
    ],
}


PART_KEYWORDS = {
    "front_bumper": [
        "front bumper",
    ],

    "rear_bumper": [
        "rear bumper",
        "back bumper",
    ],

    "door": [
        "door",
    ],

    "hood": [
        "hood",
        "bonnet",
    ],

    "windshield": [
        "windshield",
        "windscreen",
    ],

    "side_mirror": [
        "side mirror",
        "mirror",
    ],

    "headlight": [
        "headlight",
    ],

    "taillight": [
        "taillight",
        "tail light",
    ],

    "fender": [
        "fender",
    ],

    "quarter_panel": [
        "quarter panel",
    ],

    "body": [
        "body",
        "car body",
    ],
}


class KeywordClaimParser:

    def parse(
        self,
        user_claim: str,
    ) -> ParsedClaim:

        claim = str(user_claim).lower()

        issue_type = self._extract_issue(claim)
        object_part = self._extract_part(claim)

        return ParsedClaim(
            issue_type=issue_type,
            object_part=object_part,
            reason="Keyword parser match",
        )

    def _extract_issue(
        self,
        claim: str,
    ) -> str:

        for issue, keywords in ISSUE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in claim:
                    return issue

        return "unknown"

    def _extract_part(
        self,
        claim: str,
    ) -> str:

        for part, keywords in PART_KEYWORDS.items():
            for keyword in keywords:
                if keyword in claim:
                    return part

        return "unknown"