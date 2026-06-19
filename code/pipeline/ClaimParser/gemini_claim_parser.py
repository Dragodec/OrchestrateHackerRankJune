import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from models.parsed_claim import ParsedClaim
from pipeline.car_domain import (
    CAR_ISSUES,
    CAR_OBJECT_PARTS,
)

load_dotenv(
    Path(__file__).resolve().parent.parent.parent.parent / ".env"
)


class GeminiClaimParser:

    def __init__(self) -> None:

        api_key = os.getenv("GEMINI_API_KEY")

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

{sorted(CAR_ISSUES)}

Allowed object_part values:

{sorted(CAR_OBJECT_PARTS)}

Rules:

- Analyze the ENTIRE conversation.
- The customer's final clarified claim is the source of truth.
- Ignore questions asked by the agent unless the customer confirms them.
- If ambiguity is resolved later in the conversation, use the resolved value.
- If multiple parts are mentioned, choose the primary damaged part.
- Return ONLY values from the allowed lists.
- Handle multilingual conversations.
- If uncertain return "unknown".

Reason Rules:

- Reason is ONLY a debugging aid.
- Maximum 15 words.
- One sentence only.
- Explain what evidence in the conversation led to the selected values.
- Use only information explicitly present.
- Do NOT infer causes.
- Do NOT add facts.
- Do NOT explain your reasoning process.
- If both values are unknown, return:
  "Insufficient information."

Examples:

Input:
Rear bumper dent

Output:
{{
    "issue_type": "dent",
    "object_part": "rear_bumper",
    "reason": "Dent explicitly mentioned on rear bumper."
}}

Input:
Mera left side mirror toot gaya hai

Output:
{{
    "issue_type": "broken_part",
    "object_part": "side_mirror",
    "reason": "Side mirror explicitly described as broken."
}}

Input:
Customer: The back light of my car cracked.
Agent: By back light, do you mean taillight?
Customer: Yes, taillight.

Output:
{{
    "issue_type": "crack",
    "object_part": "taillight",
    "reason": "Customer clarified back light refers to taillight."
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

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        text = response.text.strip()

        start = text.find("{")
        end = text.rfind("}") + 1

        parsed_json = json.loads(
            text[start:end]
        )

        print("\nRAW PARSED JSON:")
        print(parsed_json)

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

        if issue_type not in CAR_ISSUES:
            issue_type = "unknown"

        if object_part not in CAR_OBJECT_PARTS:
            object_part = "unknown"

        # Safety guard for debug field
        reason = str(reason).strip()

        if not reason:
            reason = "Insufficient information."

        if len(reason.split()) > 20:
            reason = "Debug reason exceeded limit."

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