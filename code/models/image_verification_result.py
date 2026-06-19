from dataclasses import dataclass


@dataclass
class ImageVerificationResult:
    part_visible: bool
    damage_visible: bool
    claim_matches_image: bool
    supporting_image_ids: list[str]
    reason: str