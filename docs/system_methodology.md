# Methodology

## Problem Approach
Manual anonymization is slow, error-prone, and inconsistent. Our methodology automates this process using layered detection across both text-based and image-based datasets.

## Detection Strategy

### 1. Rule-Based Detection (Regex)
Used for high-confidence structured PII:
- Emails
- Phone numbers
- Identification numbers
- Postal codes

**Why Regex?**
✔ Fast  
✔ Deterministic  
✔ High precision for known formats  

### 2. Contextual Detection (NLP Logic)
Used for identifying:
- Personal names
- Locations
- Free-text sensitive mentions

**Why NLP?**
✔ Handles unstructured data  
✔ Detects information without fixed patterns  
✔ Improves recall where regex cannot apply  

---

### 3. OCR-Based Extraction (for Images & Scanned Files)

Some datasets contain sensitive information embedded in:
- Scanned documents
- Images
- PDFs
- Screenshots of records

To address this, we integrate **Optical Character Recognition (OCR)**.

**OCR Role in the Pipeline:**
Image/File → OCR Text Extraction → Pass to NLP + Regex Detection → Redaction

**Why OCR?**
✔ Converts visual text into machine-readable format  
✔ Enables redaction of non-editable documents  
✔ Extends privacy protection beyond structured datasets  

---

## Redaction Strategy
Instead of deleting data, we:
- Mask sensitive values
- Replace identifiers with anonymized tokens
- Preserve dataset schema and usability

Example:
`john.doe@email.com` → `[EMAIL_REDACTED]`

---

## Data Preservation Principle
Privacy is enforced **without destroying dataset value**.

The system ensures:
- Analytical integrity remains intact  
- Non-sensitive attributes are preserved  
- Data can still be used for research, analytics, or AI training