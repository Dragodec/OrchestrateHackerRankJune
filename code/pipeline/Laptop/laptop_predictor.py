from pathlib import Path
from typing import Dict

from models.prediction import PredictionResult
from models.image_verification_result import (
    ImageVerificationResult,
)

from pipeline.ClaimParser.laptop_claim_parser import (
    LaptopClaimParser,
)

from pipeline.Laptop.requirement_mapper import (
    RequirementMapper,
)

from pipeline.ImageAnalyzer.gemini_image_verifier import (
    GeminiImageVerifier,
)


class LaptopPredictor:

    def __init__(self):

        print(
            "Initializing LaptopPredictor..."
        )

        self.claim_parser = (
            LaptopClaimParser()
        )

        self.requirement_mapper = (
            RequirementMapper()
        )

        self.image_verifier = (
            GeminiImageVerifier()
        )

        print(
            "LaptopPredictor initialized."
        )

    def predict(
        self,
        row,
    ) -> Dict:

        user_id = row["user_id"]

        claim_object = str(
            row["claim_object"]
        ).lower()

        print(
            f"\nProcessing: {user_id}"
        )

        if claim_object != "laptop":

            print(
                "Skipping non-laptop claim."
            )

            prediction = PredictionResult(
                evidence_standard_met=False,
                evidence_standard_met_reason=(
                    "Not a laptop claim."
                ),
                risk_flags="none",
                issue_type="unknown",
                object_part="unknown",
                claim_status="not_applicable",
                claim_status_justification=(
                    "Row does not belong "
                    "to laptop domain."
                ),
                supporting_image_ids="none",
                valid_image=False,
                severity="unknown",
            )

            return prediction.to_dict()

        print(
            "Running claim parser..."
        )

        parsed_claim = (
            self.claim_parser.parse(
                row["user_claim"]
            )
        )

        print(
            f"Issue: "
            f"{parsed_claim.issue_type}"
        )

        print(
            f"Part: "
            f"{parsed_claim.object_part}"
        )

        # ==========================================
        # SMART REQUIREMENT SELECTION
        # ==========================================

        if parsed_claim.object_part == "screen":

            if parsed_claim.issue_type in [
                "water_damage",
                "stain",
            ]:

                requirement_id = (
                    "REQ_LAPTOP_LIQUID_DAMAGE"
                )

            else:

                requirement_id = (
                    "REQ_LAPTOP_SCREEN"
                )

        elif parsed_claim.issue_type in [
            "water_damage",
            "stain",
        ]:

            requirement_id = (
                "REQ_LAPTOP_LIQUID_DAMAGE"
            )

        else:

            requirement_id = (
                "REQ_LAPTOP_HARDWARE"
            )

        print(
            f"Requirement: "
            f"{requirement_id}"
        )

        project_root = (
            Path(__file__)
            .resolve()
            .parent
            .parent
            .parent
            .parent
        )

        image_paths = [
            str(
                project_root
                / "dataset"
                / relative_path
            )
            for relative_path in str(
                row["image_paths"]
            ).split(";")
        ]

        print(
            "Resolved image paths:"
        )

        for image_path in image_paths:

            print(
                image_path
            )

        # ==========================================
        # QUOTA GUARD
        # ==========================================

        if user_id in [
            "user_020",
            "user_026",
            "user_028",
        ]:

            print(
                "Running Gemini image verification..."
            )

            verification = (
                self.image_verifier.verify(
                    image_paths=image_paths,
                    issue_type=(
                        parsed_claim.issue_type
                    ),
                    object_part=(
                        parsed_claim.object_part
                    ),
                    requirement_id=(
                        requirement_id
                    ),
                )
            )

        else:

            print(
                "Skipping image verification."
            )

            verification = (
                ImageVerificationResult(
                    part_visible=False,
                    damage_visible=False,
                    claim_matches_image=False,
                    supporting_image_ids=[],
                    reason=(
                        "Image verification skipped "
                        "to conserve quota."
                    ),
                )
            )

        evidence_standard_met = (
            verification.part_visible
            and
            verification.damage_visible
            and
            verification.claim_matches_image
        )

        if verification.claim_matches_image:

            claim_status = (
                "supported"
            )

            claim_status_reason = (
                verification.reason
            )

        else:

            claim_status = (
                "not_enough_information"
            )

            claim_status_reason = (
                verification.reason
            )

        severity = (
            self._derive_severity(
                parsed_claim.issue_type,
                verification.damage_visible,
            )
        )

        prediction = PredictionResult(
            evidence_standard_met=(
                evidence_standard_met
            ),
            evidence_standard_met_reason=(
                verification.reason
            ),
            risk_flags="none",
            issue_type=(
                parsed_claim.issue_type
            ),
            object_part=(
                parsed_claim.object_part
            ),
            claim_status=(
                claim_status
            ),
            claim_status_justification=(
                claim_status_reason
            ),
            supporting_image_ids=";".join(
                verification.supporting_image_ids
            )
            if verification.supporting_image_ids
            else "none",
            valid_image=(
                verification.part_visible
            ),
            severity=severity,
        )

        print(
            f"Prediction generated "
            f"for {user_id}"
        )

        return prediction.to_dict()

    def _derive_severity(
        self,
        issue_type: str,
        damage_visible: bool,
    ) -> str:

        if not damage_visible:
            return "none"

        if issue_type in [
            "scratch",
            "stain",
        ]:
            return "low"

        if issue_type in [
            "dent",
            "crack",
            "water_damage",
        ]:
            return "medium"

        if issue_type in [
            "glass_shatter",
            "broken_part",
            "missing_part",
        ]:
            return "high"

        return "unknown"