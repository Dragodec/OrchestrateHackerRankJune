from pipeline.ClaimParser.claim_parser import (
    ClaimParser
)


def main() -> None:

    parser = ClaimParser()

    claims = [
        "The rear bumper has a dent after a collision.",
        "My side mirror is broken.",
        "Front bumper scratched badly.",
        "Headlight cracked after impact.",
    ]

    for claim in claims:

        result = parser.parse(claim)

        print(f"Claim: {claim}")
        print(result)
        print(f"Reason: {result.reason}")
        print("-" * 50)


if __name__ == "__main__":
    main()