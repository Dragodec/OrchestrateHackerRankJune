# scripts/test_image_verifier.py

from pipeline.ImageAnalyzer.gemini_image_verifier import (
    GeminiImageVerifier,
)


def main():

    image_paths = [
        r"D:\Orchestrate-June\Code\hackerrank-orchestrate-june26\dataset\images\test\case_003\img_1.jpg",
    ]

    verifier = GeminiImageVerifier()

    result = verifier.verify(
        image_paths=image_paths,
        issue_type="dent",
        object_part="door",
        requirement_id=(
            "REQ_CAR_BODY_PANEL"
        ),
    )

    print()
    print("Verification Result")
    print("-" * 60)

    print(
        f"Part Visible: "
        f"{result.part_visible}"
    )

    print(
        f"Damage Visible: "
        f"{result.damage_visible}"
    )

    print(
        f"Claim Matches Image: "
        f"{result.claim_matches_image}"
    )

    print(
        f"Supporting Images: "
        f"{result.supporting_image_ids}"
    )

    print(
        f"Reason: "
        f"{result.reason}"
    )

    print("-" * 60)


if __name__ == "__main__":
    main()