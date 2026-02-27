# System Design

## Overview
The AI PII Redactor is designed as a preprocessing layer that automatically detects and removes Personally Identifiable Information (PII) from datasets before they are shared, analyzed, or used for AI training.

## Architecture Flow
Upload Dataset → Preprocessing → PII Detection → Redaction → Validation → Safe Output

## Components

### 1. Data Ingestion
Accepts structured and semi‑structured files:
- Detects Names, Locations, Organizations
- Detects Phone, Email, Aadhaar (Regex)
- CSV dataset support

### 2. Preprocessing Layer
- Normalizes text
- Handles encoding issues
- Converts dataset into scan-ready format

### 3. Detection Engine
Hybrid detection approach:
- Regex → Structured identifiers
- NLP → Contextual personal information

### 4. Redaction Engine
Replaces detected PII with anonymized tokens:
- `[NAME_REDACTED]`
- `[EMAIL_MASKED]`
- `[PHONE_REMOVED]`

### 5. Validation Layer
Ensures:
- Dataset usability is preserved
- No structural corruption occurs

### 6. Output Generator
Produces a privacy-safe dataset ready for:
- Public release
- Research usage
- AI model training