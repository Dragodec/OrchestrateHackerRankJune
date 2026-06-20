import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from models.parsed_claim import ParsedClaim

from pipeline.Laptop.laptop_domain import (
    LAPTOP_ISSUES,
    LAPTOP_OBJECT_PARTS,
)

load_dotenv(
    Path(__file__).resolve().parent.parent.parent.parent / ".env"
)


class GeminiLaptopClaimParser:

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

{sorted(LAPTOP_ISSUES)}

Allowed object_part values:

{sorted(LAPTOP_OBJECT_PARTS)}

Rules:

- Analyze the ENTIRE conversation.
- The customer's final clarified claim is the source of truth.
- Ignore questions asked by the support agent unless the customer confirms them.
- If ambiguity is resolved later in the conversation, use the resolved value.
- If multiple parts are mentioned, choose the PRIMARY claimed damaged part.
- If multiple damages are mentioned, choose the PRIMARY claimed damage.
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
- If both values are unknown return:
  "Insufficient information."

Examples:

Input:
Customer: Keyboard liquid damage.
Support: Screen too?
Customer: No, keyboard only.

Output:
{{
    "issue_type": "water_damage",
    "object_part": "keyboard",
    "reason": "Customer clarified keyboard liquid damage."
}}

Input:
Customer: Hinge broke and screen cracked.
Support: Which should be reviewed?
Customer: Hinge damage.

Output:
{{
    "issue_type": "broken_part",
    "object_part": "hinge",
    "reason": "Customer selected hinge damage."
}}

Input:
Customer: I need help with a laptop body crack claim.
Support: Screen, keyboard, or body?
Customer: Body only.

Output:
{{
    "issue_type": "crack",
    "object_part": "body",
    "reason": "Customer clarified body crack claim."
}}

Input:
Customer: The trackpad is cracked.
Support: Screen too?
Customer: No, trackpad only.

Output:
{{
    "issue_type": "crack",
    "object_part": "trackpad",
    "reason": "Customer clarified trackpad damage."
}}

Input:
Customer: The laptop lid is cracked.
Support: Display or lid?
Customer: Lid only.

Output:
{{
    "issue_type": "crack",
    "object_part": "lid",
    "reason": "Customer clarified lid damage."
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
        print("\n=== GEMINI LAPTOP PARSER CALLED ===")  
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

        if issue_type not in LAPTOP_ISSUES:
            issue_type = "unknown"

        if object_part not in LAPTOP_OBJECT_PARTS:
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