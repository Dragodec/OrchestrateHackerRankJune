from typing import Dict

from models.prediction import PredictionResult
from pipeline.claim_parser import ClaimParser


PLACEHOLDER_EVIDENCE_STANDARD_MET = False
PLACEHOLDER_EVIDENCE_REASON = "Claim parsing completed. Evidence evaluation pending."

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
        self.claim_parser = ClaimParser()

    def predict(self, row) -> Dict:

        claim_object = str(row["claim_object"]).lower()

        # Only handle cars for now
        if claim_object != "car":
            parsed_issue = "unknown"
            parsed_part = "unknown"
        else:
            parsed_claim = self.claim_parser.parse(
                row["user_claim"]
            )

            parsed_issue = parsed_claim.issue_type
            parsed_part = parsed_claim.object_part

        prediction = PredictionResult(
            evidence_standard_met=PLACEHOLDER_EVIDENCE_STANDARD_MET,
            evidence_standard_met_reason=PLACEHOLDER_EVIDENCE_REASON,
            risk_flags=PLACEHOLDER_RISK_FLAGS,
            issue_type=parsed_issue,
            object_part=parsed_part,
            claim_status=PLACEHOLDER_CLAIM_STATUS,
            claim_status_justification=PLACEHOLDER_CLAIM_STATUS_REASON,
            supporting_image_ids=PLACEHOLDER_SUPPORTING_IMAGES,
            valid_image=PLACEHOLDER_VALID_IMAGE,
            severity=PLACEHOLDER_SEVERITY,
        )

        return prediction.to_dict()