from models.parsed_claim import ParsedClaim


TRANSLATIONS = {

    "caja": "box",
    "paquete": "package",
    "sello": "seal",
    "etiqueta": "label",

    "mojado": "wet",
    "rasgado": "torn",

    "toot gaya": "broken",
    "phat gaya": "torn",
    "bheeg gaya": "wet",
}


ISSUE_KEYWORDS = {

    "water_damage": [
        "water damage",
        "wet",
        "soaked",
        "rain damage",
    ],

    "stain": [
        "stain",
        "stained",
        "spill",
        "dirty",
    ],

    "missing_part": [
        "missing",
        "not included",
        "item missing",
        "contents missing",
    ],

    "crushed_packaging": [
        "crushed",
        "crumpled",
        "smashed",
        "collapsed",
    ],

    "torn_packaging": [
        "torn",
        "tear",
        "ripped",
        "opened",
        "damaged packaging",
    ],
}


PART_KEYWORDS = {

    "package_corner": [
        "corner",
        "package corner",
        "box corner",
    ],

    "package_side": [
        "side",
        "package side",
        "box side",
    ],

    "seal": [
        "seal",
        "security seal",
        "tamper seal",
    ],

    "label": [
        "label",
        "shipping label",
        "barcode",
    ],

    "contents": [
        "contents",
        "inside item",
        "inside",
    ],

    "item": [
        "item",
        "product",
    ],

    "box": [
        "box",
        "package",
        "carton",
    ],
}


class PackageKeywordClaimParser:

    def parse(
        self,
        user_claim: str,
    ) -> ParsedClaim:

        claim = str(
            user_claim
        ).lower()

        claim = self._normalize_text(
            claim
        )

        claim = (
            self._extract_final_customer_claim(
                claim
            )
        )

        issue_type = (
            self._extract_issue(
                claim
            )
        )

        object_part = (
            self._extract_part(
                claim
            )
        )

        return ParsedClaim(
            issue_type=issue_type,
            object_part=object_part,
            reason="Keyword parser match",
        )

    def _normalize_text(
        self,
        claim: str,
    ) -> str:

        for foreign, english in (
            TRANSLATIONS.items()
        ):

            claim = claim.replace(
                foreign,
                english,
            )

        return claim

    def _extract_final_customer_claim(
        self,
        claim: str,
    ) -> str:

        segments = claim.split("|")

        customer_lines = []

        for segment in segments:

            segment = segment.strip()

            if segment.startswith(
                "customer:"
            ):
                customer_lines.append(
                    segment
                )

        if customer_lines:
            return customer_lines[-1]

        return claim

    def _extract_issue(
        self,
        claim: str,
    ) -> str:

        for issue, keywords in (
            ISSUE_KEYWORDS.items()
        ):

            for keyword in keywords:

                if keyword in claim:
                    return issue

        return "unknown"

    def _extract_part(
        self,
        claim: str,
    ) -> str:

        for part, keywords in (
            PART_KEYWORDS.items()
        ):

            for keyword in keywords:

                if keyword in claim:
                    return part

        return "unknown"