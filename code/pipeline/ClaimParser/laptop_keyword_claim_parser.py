from models.parsed_claim import ParsedClaim


TRANSLATIONS = {
    "pantalla": "screen",
    "teclas": "keyboard",
    "tecla": "key",
    "faltan": "missing",

    "pantalla rota": "cracked screen",
    "pantalla quebrada": "cracked screen",

    "toot gaya": "broken",
    "toot gyi": "broken",
}


ISSUE_KEYWORDS = {

    # Highest priority first

    "water_damage": [
        "liquid damage",
        "water damage",
    ],

    "stain": [
        "liquid stain",
        "stain",
        "stained",
        "coffee",
        "spill",
        "spilled",
        "sticky",
    ],

    "glass_shatter": [
        "shattered screen",
        "screen shattered",
        "shattered",
    ],

    "missing_part": [
        "missing",
        "came off",
        "fell off",
        "lost",
    ],

    "broken_part": [
        "broken",
        "broke",
        "wobbles",
    ],

    "crack": [
        "crack",
        "cracked",
    ],

    "dent": [
        "dent",
        "dented",
    ],

    "scratch": [
        "scratch",
        "scratched",
    ],
}


PART_KEYWORDS = {

    # Most specific first

    "trackpad": [
        "trackpad",
        "touchpad",
    ],

    "hinge": [
        "hinge",
    ],

    "keyboard": [
        "keyboard",
        "keycaps",
        "keys",
        "key",
    ],

    "lid": [
        "lid",
    ],

    "corner": [
        "corner",
    ],

    "port": [
        "usb port",
        "charging port",
        "port",
    ],

    "base": [
        "underside",
        "bottom",
        "base",
    ],

    "body": [
        "outer body",
        "side edge",
        "body only",
        "body",
    ],

    "screen": [
        "screen",
        "display",
    ],
}


class LaptopKeywordClaimParser:

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