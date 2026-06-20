from models.parsed_claim import ParsedClaim

from pipeline.ClaimParser.gemini_package_claim_parser import (
    GeminiPackageClaimParser,
)

from pipeline.ClaimParser.package_keyword_claim_parser import (
    PackageKeywordClaimParser,
)


class PackageClaimParser:

    def __init__(
        self,
    ) -> None:

        self.keyword_parser = (
            PackageKeywordClaimParser()
        )

        self.gemini_parser = (
            GeminiPackageClaimParser()
        )

    def parse(
        self,
        user_claim: str,
    ) -> ParsedClaim:

        return self.gemini_parser.parse(
            user_claim
        )