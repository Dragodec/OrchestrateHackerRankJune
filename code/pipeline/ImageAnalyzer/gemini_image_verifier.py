# pipeline/ImageAnalyzer/gemini_image_verifier.py

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from models.image_verification_result import (
    ImageVerificationResult,
)

load_dotenv(
    Path(__file__).resolve().parent.parent.parent.parent / ".env"
)


class GeminiImageVerifier:

    def __init__(self):

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        print(
            f"API Key Found: {bool(api_key)}"
        )

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def verify(
        self,
        image_paths: list[str],
        issue_type: str,
        object_part: str,
        requirement_id: str,
    ) -> ImageVerificationResult:

        contents = []

        prompt = f"""
You are an insurance image verifier.

Claim:

issue_type = {issue_type}
object_part = {object_part}

Requirement:

{requirement_id}

Task:

1. Is the claimed part visible?
2. Is the claimed damage visible?
3. Does the image support the claim?
4. Which image(s) support the claim?

Rules:

- Use only visible evidence.
- Do not assume damage exists.
- Do not infer hidden damage.
- If unsure, return false.
- supporting_image_ids must use:
  img_1, img_2, img_3, ...

Return ONLY JSON:

{{
    "part_visible": true,
    "damage_visible": true,
    "claim_matches_image": true,
    "supporting_image_ids": ["img_1"],
    "reason": "Rear bumper dent visible."
}}
"""

        contents.append(prompt)

        for image_path in image_paths:

            uploaded_file = self.client.files.upload(
                file=image_path
            )

            contents.append(
                uploaded_file
            )

        response = (
            self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
            )
        )

        text = response.text.strip()

        start = text.find("{")
        end = text.rfind("}") + 1

        parsed_json = json.loads(
            text[start:end]
        )

        return ImageVerificationResult(
            part_visible=parsed_json.get(
                "part_visible",
                False,
            ),
            damage_visible=parsed_json.get(
                "damage_visible",
                False,
            ),
            claim_matches_image=parsed_json.get(
                "claim_matches_image",
                False,
            ),
            supporting_image_ids=parsed_json.get(
                "supporting_image_ids",
                [],
            ),
            reason=parsed_json.get(
                "reason",
                "No reason provided.",
            ),
        )