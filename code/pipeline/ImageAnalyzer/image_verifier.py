from models.image_verification_result import (
    ImageVerificationResult,
)


class ImageVerifier:

    def verify(
        self,
        image_paths: list[str],
        issue_type: str,
        object_part: str,
        requirement_id: str,
    ) -> ImageVerificationResult:

        return ImageVerificationResult(
            part_visible=False,
            damage_visible=False,
            claim_matches_image=False,
            supporting_image_ids=[],
            reason="Image verification not implemented.",
        )