from pipeline.ClaimParser.gemini_claim_parser import (
    GeminiClaimParser,
)


def main():

    parser = GeminiClaimParser()

    claims = [
        "Rear bumper dent",
        "Mera left side mirror toot gaya hai",
        "El parachoques trasero esta dañado",
        "Windshield shattered",
    ]

    for claim in claims:

        result = parser.parse(claim)

        print()
        print(claim)
        print(result)
        print(f"Reason: {result.reason}")
        print("-" * 60)


if __name__ == "__main__":
    main()