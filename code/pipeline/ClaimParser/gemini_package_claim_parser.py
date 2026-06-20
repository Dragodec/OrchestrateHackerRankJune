import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from models.parsed_claim import ParsedClaim

from pipeline.Package.package_domain import (
    PACKAGE_ISSUES,
    PACKAGE_OBJECT_PARTS,
)

load_dotenv(
    Path(__file__).resolve().parent.parent.parent.parent / ".env"
)


class GeminiPackageClaimParser:

    def __init__(self) -> None:

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:

            raise ValueError(
                "GEMINI_API_KEY not found in .env"
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def parse(
        self,
        user_claim: str,
    ) -> ParsedClaim:

        prompt = f"""
You are an insurance claim parser.

Extract:

1. issue_type
2. object_part
3. reason

Allowed issue_type values:

{sorted(PACKAGE_ISSUES)}

Allowed object_part values:

{sorted(PACKAGE_OBJECT_PARTS)}

Rules:

- Analyze the ENTIRE conversation.
- The customer's final clarified claim is the source of truth.
- Ignore support questions unless customer confirms.
- Return ONLY allowed values.
- Handle multilingual conversations.
- If uncertain return "unknown".

Reason Rules:

- Maximum 15 words.
- One sentence.
- Use only conversation evidence.
- Do not infer hidden damage.
- If both values unknown:
  "Insufficient information."

Examples:

Input:
Customer: The package corner got crushed.

Output:
{{
    "issue_type": "crushed_packaging",
    "object_part": "package_corner",
    "reason": "Customer reported crushed package corner."
}}

Input:
Customer: The seal was torn.

Output:
{{
    "issue_type": "torn_packaging",
    "object_part": "seal",
    "reason": "Customer reported torn seal."
}}

Input:
Customer: Rain soaked the box.

Output:
{{
    "issue_type": "water_damage",
    "object_part": "box",
    "reason": "Customer reported water damaged box."
}}

Input:
Customer: The item inside was missing.

Output:
{{
    "issue_type": "missing_part",
    "object_part": "contents",
    "reason": "Customer reported missing contents."
}}

Input:
Customer: Label is stained.

Output:
{{
    "issue_type": "stain",
    "object_part": "label",
    "reason": "Customer reported stained label."
}}

Return ONLY JSON:

{{
    "issue_type": "...",
    "object_part": "...",
    "reason": "..."
}}

Conversation:

{user_claim}
"""

        print(
            "\n=== GEMINI PACKAGE PARSER CALLED ==="
        )

        response = (
            self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
        )

        text = response.text.strip()

        start = text.find("{")
        end = text.rfind("}") + 1

        parsed_json = json.loads(
            text[start:end]
        )

        print(
            "\nRAW PARSED JSON:"
        )

        print(
            parsed_json
        )

        issue_type = parsed_json.get(
            "issue_type",
            "unknown",
        )

        object_part = parsed_json.get(
            "object_part",
            "unknown",
        )

        reason = parsed_json.get(
            "reason",
            "Insufficient information.",
        )

        if issue_type not in PACKAGE_ISSUES:
            issue_type = "unknown"

        if object_part not in PACKAGE_OBJECT_PARTS:
            object_part = "unknown"

        reason = str(
            reason
        ).strip()

        if not reason:
            reason = (
                "Insufficient information."
            )

        if len(
            reason.split()
        ) > 20:
            reason = (
                "Debug reason exceeded limit."
            )

        print(
            f"Issue: {issue_type}"
        )

        print(
            f"Part: {object_part}"
        )

        print(
            f"Reason: {reason}"
        )

        print("=" * 60)

        return ParsedClaim(
            issue_type=issue_type,
            object_part=object_part,
            reason=reason,
        )