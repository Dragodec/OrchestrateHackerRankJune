# Multi-Modal Insurance Claim Validation System

## Overview

This project is a multi-modal claim validation pipeline that analyzes both customer conversations and supporting images to determine whether an insurance claim is supported by visual evidence.

The system processes claims across multiple domains such as:

* Vehicle Damage Claims
* Laptop Damage Claims
* Package Delivery Claims

For each claim, the pipeline:

1. Extracts structured information from customer-agent conversations.
2. Identifies the claimed object and damage type.
3. Analyzes uploaded images using a Vision LLM.
4. Validates whether the visual evidence supports the claim.
5. Generates a structured CSV output for downstream review.

---

## Approach

### Phase 1: Claim Understanding

Customer conversations are parsed to extract:

* Claim Object (Car, Laptop, Package)
* Claimed Damage
* Affected Part
* Claim Type

Example:

Customer says:

> "The laptop screen has a crack on the left side."

Parsed Output:

```json
{
  "claim_object": "laptop",
  "issue_type": "cracked",
  "object_part": "screen"
}
```

---

### Phase 2: Image Evidence Analysis

Relevant images are sent to a Vision LLM.

The model answers:

* Is the claimed object visible?
* Is the claimed damage visible?
* Does the image support the claim?
* Which images provide evidence?

Example Output:

```json
{
  "part_visible": true,
  "damage_visible": true,
  "claim_matches_image": true,
  "supporting_image_ids": ["img_1"]
}
```

---

### Phase 3: Claim Validation

Conversation understanding and image evidence are combined to determine:

* Evidence Standard Met
* Claim Status
* Risk Flags
* Supporting Images

Example:

| Claim          | Evidence      |
| -------------- | ------------- |
| Screen Crack   | Visible Crack |
| Package Opened | Visible Tear  |
| Car Dent       | Visible Dent  |

Result:

```json
{
  "evidence_standard_met": true,
  "claim_status": "supported"
}
```

---

## Pipeline Flow

```text
Claims CSV
    │
    ▼
Claim Parser
    │
    ▼
Structured Claim
    │
    ▼
Image Analyzer
    │
    ▼
Evidence Validator
    │
    ▼
Output Generator
    │
    ▼
myOutput.csv
```

---

## Project Structure

```text
project/
│
├── data/
│   ├── claims.csv
│   └── images/
│
├── pipeline/
│   ├── claim_parser.py
│   ├── image_analyzer.py
│   ├── predictor_factory.py
│   ├── validators/
│   └── output_generator.py
│
├── outputs/
│   └── myOutput.csv
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd project
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

Windows:

```bash
.venv\Scripts\activate
```

Linux / Mac:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Running the Pipeline

```bash
python main.py
```

or

```bash
python run.py
```

Depending on repository structure.

The pipeline will:

1. Read `claims.csv`
2. Analyze associated images
3. Validate claims
4. Generate:

```text
myOutput.csv
```

---

## Output Format

Example columns:

```text
user_id
image_paths
user_claim
claim_object
evidence_standard_met
evidence_standard_met_reason
risk_flags
issue_type
object_part
claim_status
claim_status_justification
supporting_image_ids
valid_image
severity
```

---

## Design Goals

* Modular architecture
* Multi-domain support
* Batch processing
* Recoverable execution
* Structured outputs
* LLM-powered visual validation
* Easy extension to new claim types

---

## Future Improvements

* Confidence scoring
* OCR-based evidence extraction
* Multiple image ranking
* Fraud detection signals
* Human review workflow
* Fine-tuned domain-specific models
