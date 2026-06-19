from pipeline.parsed_claim import ParsedClaim

from pipeline.ClaimParser.gemini_claim_parser import (
    GeminiClaimParser,
)

from pipeline.ClaimParser.keyword_claim_parser import (
    KeywordClaimParser,
)


class ClaimParser:

    def __init__(self) -> None:

        self.keyword_parser = KeywordClaimParser()

        self.gemini_parser = GeminiClaimParser()

    def parse(
        self,
        user_claim: str,
    ) -> ParsedClaim:

        keyword_result = self.keyword_parser.parse(
            user_claim
        )

        if (
            keyword_result.issue_type != "unknown"
            and
            keyword_result.object_part != "unknown"
        ):
            return keyword_result

        try:

            gemini_result = self.gemini_parser.parse(
                user_claim
            )

            if (
                gemini_result.issue_type == "unknown"
                and
                gemini_result.object_part == "unknown"
            ):
                return keyword_result

            return gemini_result

        except Exception as e:

            print(
                "Gemini parser failed. "
                "Falling back to keyword parser. "
                f"Error: {e}"
            )

            return keyword_result