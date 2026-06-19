from dataclasses import dataclass


@dataclass
class ParsedClaim:
    issue_type: str
    object_part: str
    reason: str 