from models.parsed_claim import ParsedClaim

from pipeline.ClaimParser.gemini_laptop_claim_parser import (
    GeminiLaptopClaimParser,
)

from pipeline.ClaimParser.laptop_keyword_claim_parser import (
    LaptopKeywordClaimParser,
)


class LaptopClaimParser:

    def __init__(
        self,
    ) -> None:

        self.keyword_parser = (
            LaptopKeywordClaimParser()
        )

        self.gemini_parser = (
            GeminiLaptopClaimParser()
        )

    def parse(
        self,
        user_claim: str,
    ) -> ParsedClaim:

        return self.gemini_parser.parse(
            user_claim
        )