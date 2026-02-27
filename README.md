 
 # AI PII REDACTOR FOR PUBLIC DATASETS

1. # PROBLEM STATEMENT ADDRESSED

Organizations frequently publish datasets for research, analytics, or AI training without properly removing Personally Identifiable Information (PII) such as names, phone numbers, emails, Aadhaar numbers, and addresses.

This leads to:
• Privacy violations
• Risk of identity theft
• Legal non-compliance with data protection regulations
• Unsafe data being used in public repositories or AI models

There is a need for an automated system that detects and redacts sensitive information before datasets are shared publicly.

2. # PROPOSED SOLUTION


The proposed solution is an AI-Assisted PII Redaction System designed to automatically detect, assess, and sanitize sensitive information in datasets before they are shared publicly or used for AI model training.

Instead of relying on slow and error-prone manual review, this system acts as an automated privacy filter that ensures datasets are compliant, secure, and safe for distribution.



3. # APPROACH

We built a lightweight Privacy Compliance Tool that acts as a “data safety layer” before datasets are released.

Workflow:

1. User uploads a dataset (CSV / TXT / Excel).
2. The system scans content using Regex-based pattern detection and NLP concepts.
3. Sensitive entities such as phone numbers, emails, IDs, and addresses are identified.
4. Detected PII is automatically replaced with safe placeholders (e.g., [REDACTED]).
5. A Risk Score is generated based on how much sensitive data was found.
6. A clean, compliance-ready dataset is generated for download.

This ensures datasets are safe for:
• Public sharing
• Research publishing
• AI/LLM training pipelines

4. # TECH STACK USED

• Python – Core programming language used to build the redaction engine and processing logic.

• Streamlit – Provides the web-based interface for uploading datasets and viewing redacted outputs interactively.

• Pandas – Handles structured data processing, cleaning, transformation, and file format support (CSV/Excel).

• Regex (re module) – Performs rule-based detection of structured PII such as emails, phone numbers, and IDs.

• OpenPyXL – Enables reading and writing Excel (.xlsx) dataset files.

• Groq API – Used for fast LLM-based contextual analysis to detect sensitive information in unstructured text.

• python-dotenv – Manages environment variables securely (API keys, configuration settings).

• pdfplumber – Extracts text from PDF documents for scanning and redaction.

• python-docx – Processes Microsoft Word (.docx) files to detect and redact sensitive content.

• pytesseract – Performs OCR (Optical Character Recognition) to extract text from images or scanned documents.

• Pillow (PIL) – Supports image preprocessing required for OCR operations.

• ReportLab – Generates clean, redacted PDF outputs after processing.

5. # THIRD-PARTY TOOLS USED

 Tool: Streamlit
License: Apache License 2.0
Usage: Provides the web-based interface for uploading datasets and displaying redacted outputs interactively.

Tool: Groq (LLM Inference API)
License: Proprietary (API-based usage)
Usage: Enables fast AI-assisted entity detection and contextual understanding for identifying sensitive information beyond regex patterns.

Tool: python-dotenv
License: BSD 3-Clause License
Usage: Manages environment variables securely (e.g., API keys) without hardcoding them into the source code.

Tool: pdfplumber
License: MIT License
Usage: Extracts text from PDF documents so that PII detection can be applied to unstructured files.

Tool: python-docx
License: MIT License
Usage: Reads and processes Microsoft Word (.docx) files for scanning and redaction of sensitive content.

Tool: pandas
License: BSD 3-Clause License
Usage: Handles structured dataset processing, transformation, and export of cleaned data files.

Tool: reportlab
License: BSD License
Usage: Generates redacted PDF outputs and compliance-ready reports.

Tool: pytesseract
License: Apache License 2.0
Usage: Performs OCR (Optical Character Recognition) to detect text from scanned documents and images before applying PII redaction.

Tool: Pillow (PIL)
License: Historical Permission Notice and Disclaimer (HPND)
Usage: Supports image preprocessing required for OCR and redaction workflows.

6. # SETUP INSTRUCTIONS

Follow these steps to run the project locally:

Step 1: Clone the repository
git clone <your-repo-url>
cd <project-folder>

Step 2: Create a virtual environment  
python -m venv venv

Activate environment:
Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate

Step 3: Install dependencies
pip install -r requirements.txt

Step 4: Run the application
streamlit run app.py

Step 5: Open the browser link shown in the terminal to use the tool.

7. # TEAM MEMBERS & ROLES

Member 1:  Akshath
Role: Project Design, UI Development, Integration

Member 2:  Srinath
Role: PII Detection Logic, Regex Implementation

Member 3:   Vaishnavi
Role: Data Processing, Redaction Engine

Member 4:   Akhiranandan
Role: Testing, Demo Preparation

## PROJECT SUMMARY

AI PII Redactor is a privacy-first system that ensures sensitive information is automatically removed before datasets enter public ecosystems or AI pipelines. It enables organizations to share data responsibly while maintaining compliance and protecting individual privacy.
