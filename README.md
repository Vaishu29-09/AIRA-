 
 # AI PII REDACTOR FOR PUBLIC DATASETS

1. # PROBLEM STATEMENT ADDRESSED

Organizations frequently publish datasets for research, analytics, or AI training without properly removing Personally Identifiable Information (PII) such as names, phone numbers, emails, Aadhaar numbers, and addresses.

This leads to:
• Privacy violations
• Risk of identity theft
• Legal non-compliance with data protection regulations
• Unsafe data being used in public repositories or AI models

There is a need for an automated system that detects and redacts sensitive information before datasets are shared publicly.

2. # APPROACH

---

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

3. # TECH STACK USED

---

• Python – Core programming language
• Streamlit – Web-based user interface
• Pandas – Dataset handling and processing
• Regex (re module) – Pattern-based PII detection
• OpenPyXL – Excel file support

4. # THIRD-PARTY TOOLS USED

---

Tool: Streamlit
License: Apache License 2.0
Usage: Used to create the interactive UI for uploading and processing datasets.

Tool: Pandas
License: BSD 3-Clause License
Usage: Used for structured data processing and transformation.

Tool: OpenPyXL
License: MIT License
Usage: Used for reading Excel dataset files.

(All tools used are open-source and compliant for academic and hackathon use.)

5. # SETUP INSTRUCTIONS

---

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

6. TEAM MEMBERS & ROLES

Member 1:  
Role: Project Design, UI Development, Integration

Member 2:  
Role: PII Detection Logic, Regex Implementation

Member 3:   
Role: Data Processing, Redaction Engine

Member 4:   
Role: Testing, Documentation, Demo Preparation

## PROJECT SUMMARY

AI PII Redactor is a privacy-first system that ensures sensitive information is automatically removed before datasets enter public ecosystems or AI pipelines. It enables organizations to share data responsibly while maintaining compliance and protecting individual privacy.
