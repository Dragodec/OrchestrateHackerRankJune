from typing import Dict

from models.prediction import PredictionResult
from pipeline.ClaimParser.claim_parser import (
    ClaimParser
)


PLACEHOLDER_EVIDENCE_STANDARD_MET = False
PLACEHOLDER_EVIDENCE_REASON = (
    "Claim parsing completed. Evidence evaluation pending."
)

PLACEHOLDER_RISK_FLAGS = "none"

PLACEHOLDER_CLAIM_STATUS = "not_enough_information"
PLACEHOLDER_CLAIM_STATUS_REASON = (
    "Image analysis not implemented yet."
)

PLACEHOLDER_SUPPORTING_IMAGES = "none"
PLACEHOLDER_VALID_IMAGE = True

PLACEHOLDER_SEVERITY = "unknown"


class CarPredictor:

    def __init__(self):

        print("Initializing CarPredictor...")

        self.claim_parser = ClaimParser()

        print("ClaimParser initialized.")

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

        print(
            f"Claim Object: {claim_object}"
        )

        if claim_object != "car":

            print(
                "Skipping non-car claim."
            )

            parsed_issue = "unknown"
            parsed_part = "unknown"

        else:

            print(
                "Running claim parser..."
            )

            parsed_claim = self.claim_parser.parse(
                row["user_claim"]
            )

            parsed_issue = (
                parsed_claim.issue_type
            )

            parsed_part = (
                parsed_claim.object_part
            )

            print(
                f"Parsed Issue: {parsed_issue}"
            )

            print(
                f"Parsed Part: {parsed_part}"
            )

        prediction = PredictionResult(
            evidence_standard_met=PLACEHOLDER_EVIDENCE_STANDARD_MET,
            evidence_standard_met_reason=PLACEHOLDER_EVIDENCE_REASON,
            risk_flags=PLACEHOLDER_RISK_FLAGS,
            issue_type=parsed_issue,
            object_part=parsed_part,
            claim_status=PLACEHOLDER_CLAIM_STATUS,
            claim_status_justification=(
                PLACEHOLDER_CLAIM_STATUS_REASON
            ),
            supporting_image_ids=(
                PLACEHOLDER_SUPPORTING_IMAGES
            ),
            valid_image=PLACEHOLDER_VALID_IMAGE,
            severity=PLACEHOLDER_SEVERITY,
        )

        print(
            f"Prediction generated for {user_id}"
        )

        return prediction.to_dict()