import streamlit as st
from groq import Groq
import re
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY", "")

try:
    import pdfplumber
except: pdfplumber = None
try:
    import docx
except: docx = None
try:
    import pandas as pd
except: pd = None

st.set_page_config(
    page_title="ShieldPII",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Syne:wght@700;800&display=swap');

* { font-family: 'DM Sans', sans-serif; box-sizing: border-box; }

/* BASE */
html, body, .main, .block-container, [data-testid="stAppViewContainer"] {
    background-color: #0D0D0D !important;
    color: #E0E0E0 !important;
}
.block-container { padding: 0 2rem 2rem !important; max-width: 100% !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }

/* SIDEBAR */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] * {
    background-color: #080808 !important;
}
section[data-testid="stSidebar"] { border-right: 1px solid #1E1E1E !important; }

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: #1A1A1A !important;
    border-radius: 12px !important;
    padding: 5px !important;
    gap: 4px !important;
    border: 1px solid #2A2A2A !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: #666666 !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 10px 28px !important;
}
.stTabs [aria-selected="true"] {
    background: #222222 !important;
    color: #22C55E !important;
    font-weight: 700 !important;
}

/* TEXT AREA */
.stTextArea textarea {
    background: #111111 !important;
    color: #D4D4D4 !important;
    border: 1.5px solid #2A2A2A !important;
    border-radius: 12px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12.5px !important;
    line-height: 1.8 !important;
    padding: 16px !important;
}
.stTextArea textarea:focus {
    border-color: #22C55E !important;
    box-shadow: 0 0 0 3px rgba(34,197,94,0.1) !important;
}

/* FILE UPLOADER */
[data-testid="stFileUploadDropzone"] {
    background: #111111 !important;
    border: 2px dashed #2A2A2A !important;
    border-radius: 12px !important;
    color: #666666 !important;
}

/* BUTTONS */
.stButton > button {
    background: #22C55E !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 13px 28px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    width: 100% !important;
    letter-spacing: -0.2px !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: #16A34A !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(34,197,94,0.25) !important;
}
.stDownloadButton > button {
    background: #141414 !important;
    color: #E0E0E0 !important;
    border: 1.5px solid #2A2A2A !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    border-color: #22C55E !important;
    color: #22C55E !important;
    background: #0A1A0F !important;
}

/* ALERTS */
.stAlert { border-radius: 10px !important; }
[data-testid="stSuccessMessage"] { background: #052E16 !important; color: #4ADE80 !important; }
[data-testid="stErrorMessage"] { background: #450A0A !important; color: #F87171 !important; }

/* EXPANDER */
[data-testid="stExpander"] {
    background: #111111 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 12px !important;
}

/* SPINNER */
.stSpinner { color: #22C55E !important; }

/* CUSTOM COMPONENTS */
.sb-logo {
    padding: 28px 20px 22px;
    border-bottom: 1px solid #1A1A1A;
}
.sb-logo-icon {
    width: 42px; height: 42px;
    background: #22C55E;
    border-radius: 10px;
    display: flex; align-items: center;
    justify-content: center;
    font-size: 20px; margin-bottom: 12px;
}
.sb-logo-name {
    font-family: 'Syne', sans-serif;
    font-size: 20px; font-weight: 800;
    color: #F0F0F0; letter-spacing: -0.5px;
}
.sb-logo-sub { font-size: 11px; color: #444; margin-top: 2px; }

.sb-status {
    margin: 14px 20px;
    padding: 9px 13px;
    border-radius: 8px;
    font-size: 12px; font-weight: 500;
    display: flex; align-items: center; gap: 8px;
}
.sb-status.ok { background: #052E16; color: #4ADE80; border: 1px solid #14532D; }
.sb-status.err { background: #450A0A; color: #F87171; border: 1px solid #7F1D1D; }
.sb-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

.sb-section { padding: 16px 20px; border-bottom: 1px solid #1A1A1A; }
.sb-section-title { font-size: 10px; font-weight: 600; color: #3A3A3A; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 10px; }

.file-chip {
    display: inline-flex; align-items: center; gap: 5px;
    background: #141414; border: 1px solid #222;
    border-radius: 6px; padding: 5px 9px;
    font-size: 11px; color: #888; margin: 3px;
}
.file-chip b { color: #CCC; }

.rule-row { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #161616; }
.rule-row:last-child { border: none; }
.rule-name { font-size: 12px; color: #888; }
.rule-mask { font-family: 'DM Mono', monospace; font-size: 11px; color: #22C55E; }

.page-header {
    background: #0A0A0A;
    border: 1px solid #1E1E1E;
    padding: 32px 36px;
    border-radius: 16px;
    margin-bottom: 28px;
    position: relative; overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute; top: -80px; right: -80px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(34,197,94,0.08) 0%, transparent 65%);
}
.header-eyebrow { font-size: 11px; font-weight: 600; color: #22C55E; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 8px; }
.header-title { font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 800; color: #F0F0F0; line-height: 1.1; letter-spacing: -1px; margin-bottom: 10px; }
.header-title span { color: #22C55E; }
.header-sub { font-size: 14px; color: #555; max-width: 480px; line-height: 1.6; }
.header-pills { display: flex; gap: 8px; margin-top: 18px; flex-wrap: wrap; }
.pill { background: #141414; border: 1px solid #222; border-radius: 20px; padding: 4px 12px; font-size: 11px; color: #666; }
.pill b { color: #CCC; }

.steps-row { display: flex; gap: 10px; margin-bottom: 22px; }
.step { flex: 1; background: #111; border: 1px solid #1E1E1E; border-radius: 12px; padding: 16px; }
.step-n { font-family: 'Syne', sans-serif; font-size: 26px; font-weight: 800; color: #333333; margin-bottom: 6px; }
.step-t { font-size: 13px; font-weight: 600; color: #CCC; margin-bottom: 3px; }
.step-s { font-size: 11px; color: #444; }

.slabel { font-size: 11px; font-weight: 600; color: #555; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
.dot-red { width: 6px; height: 6px; background: #EF4444; border-radius: 50%; display: inline-block; }
.dot-green { width: 6px; height: 6px; background: #22C55E; border-radius: 50%; display: inline-block; }
.dot-blue { width: 6px; height: 6px; background: #60A5FA; border-radius: 50%; display: inline-block; }

.out-safe {
    background: #071A0F;
    border: 1.5px solid #14532D;
    border-radius: 12px; padding: 18px 20px;
    font-family: 'DM Mono', monospace;
    font-size: 12.5px; color: #4ADE80;
    white-space: pre-wrap; line-height: 1.8; min-height: 240px;
}
.out-restored {
    background: #070F1A;
    border: 1.5px solid #1E3A5F;
    border-radius: 12px; padding: 18px 20px;
    font-family: 'DM Mono', monospace;
    font-size: 12.5px; color: #60A5FA;
    white-space: pre-wrap; line-height: 1.8; min-height: 240px;
}
.out-placeholder {
    background: #0D0D0D;
    border: 1.5px dashed #222;
    border-radius: 12px; padding: 18px 20px;
    font-size: 13px; color: #333;
    min-height: 240px; display: flex;
    align-items: center; justify-content: center;
    text-align: center; line-height: 1.8;
}

.metrics-row { display: flex; gap: 12px; margin: 22px 0; }
.metric-card { flex: 1; background: #111; border: 1px solid #1E1E1E; border-radius: 14px; padding: 18px 14px; text-align: center; }
.metric-card.high { border-top: 3px solid #EF4444; }
.metric-card.medium { border-top: 3px solid #F59E0B; }
.metric-card.low { border-top: 3px solid #22C55E; }
.metric-card.neutral { border-top: 3px solid #444; }
.m-label { font-size: 10px; font-weight: 600; color: #444; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 8px; }
.m-val-high { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; color: #EF4444; }
.m-val-medium { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; color: #F59E0B; }
.m-val-low { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; color: #22C55E; }
.m-val-neutral { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; color: #888; }

.pii-wrap { background: #0D0D0D; border: 1px solid #1E1E1E; border-radius: 14px; overflow: hidden; }
.pii-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.pii-table th { background: #111; color: #444; padding: 12px 18px; text-align: left; font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.07em; border-bottom: 1px solid #1E1E1E; }
.pii-table td { padding: 12px 18px; border-bottom: 1px solid #141414; vertical-align: middle; }
.pii-table tr:last-child td { border-bottom: none; }
.pii-table tr:hover td { background: #111; }
.chip { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 500; }
.chip-type { background: #1E1B4B; color: #A5B4FC; }
.chip-orig { background: #450A0A; color: #F87171; font-family: 'DM Mono', monospace; }
.chip-mask { background: #052E16; color: #4ADE80; font-family: 'DM Mono', monospace; }

.summary-card { background: #0D0D0D; border: 1px solid #1E1E1E; border-left: 4px solid #22C55E; border-radius: 0 12px 12px 0; padding: 14px 18px; font-size: 14px; color: #999; line-height: 1.6; }

.divider { height: 1px; background: #1A1A1A; margin: 22px 0; }
</style>
""", unsafe_allow_html=True)

# ── File Reader ───────────────────────────────────────────────────────────────
def read_file(f):
    ext = f.name.split(".")[-1].lower()
    if ext == "txt": return f.read().decode("utf-8")
    elif ext == "pdf":
        if not pdfplumber: return "ERROR:pdfplumber"
        txt = ""
        with pdfplumber.open(f) as pdf:
            for p in pdf.pages: txt += p.extract_text() or ""
        return txt
    elif ext == "docx":
        if not docx: return "ERROR:python-docx"
        d = docx.Document(f)
        return "\n".join([p.text for p in d.paragraphs])
    elif ext == "csv":
        if not pd: return "ERROR:pandas"
        return pd.read_csv(f).to_string()
    return ""

def smart_mask(t, v):
    t = t.lower(); digits = re.sub(r'\D','',str(v))
    if "aadhaar" in t or "aadhar" in t:
        return (digits[:4]+" XXXX XXXX") if len(digits)>=4 else "XXXX XXXX XXXX"
    if "bank" in t or "account" in t:
        return (digits[:6]+"X"*(len(digits)-6)) if len(digits)>=6 else "XXXXXXXXXXXXXX"
    if "phone" in t or "mobile" in t: return "XXXXXXXXXX"
    if "name" in t: return "XXXXX XXXXX"
    if "dob" in t or "birth" in t or "date" in t: return "XX/XX/XXXX"
    if "password" in t: return "XXXXXXXX"
    if "email" in t: return "XXXXX@XXXXX.XXX"
    return None

# ── Session ───────────────────────────────────────────────────────────────────
if "pii_mapping" not in st.session_state: st.session_state.pii_mapping = {}
if "redacted_text" not in st.session_state: st.session_state.redacted_text = ""

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-icon">🛡️</div>
        <div class="sb-logo-name">ShieldPII</div>
        <div class="sb-logo-sub">AI Privacy Guard · Problem #61</div>
    </div>
    """, unsafe_allow_html=True)

    if api_key:
        st.markdown('<div class="sb-status ok"><div class="sb-dot"></div>API Connected & Ready</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sb-status err"><div class="sb-dot"></div>API key missing in .env</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-section">
        <div class="sb-section-title">Supported Formats</div>
        <div class="file-chip">📄 <span>TXT</span></div>
        <div class="file-chip">📕 <span>PDF</span></div>
        <div class="file-chip">📝 <span>DOCX</span></div>
        <div class="file-chip">📊 <span>CSV</span></div>
    </div>
    """, unsafe_allow_html=True)

    rules = [("Name","XXXXX XXXXX"),("DOB","XX/XX/XXXX"),("Phone","XXXXXXXXXX"),
             ("Email","XXXXX@XXXXX.XXX"),("Aadhaar","1234 XXXX XXXX"),
             ("Bank Account","123456XXXXXX"),("Password","XXXXXXXX")]

    st.markdown('<div class="sb-section"><div class="sb-section-title">Redaction Rules</div>', unsafe_allow_html=True)
    for name, mask in rules:
        st.markdown(f'<div class="rule-row"><span class="rule-name">{name}</span><span class="rule-mask">{mask}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:20px 24px;font-size:11px;color:#333;">
        <div style="color:#262626;font-weight:600;margin-bottom:4px;">KLH Hack with AI 2026</div>
        Privacy & Compliance Automation
    </div>
    """, unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="header-eyebrow">● AI-Powered Privacy Protection</div>
    <div class="header-title">Detect. Mask.<br><span>Restore.</span></div>
    <div class="header-sub">Upload any document and instantly redact sensitive personal data. Restore the original anytime using your secure mapping file.</div>
    <div class="header-pills">
        <div class="pill">🔒 <b>7 PII Types</b> Detected</div>
        <div class="pill">📁 <b>4 File Formats</b> Supported</div>
        <div class="pill">⚡ <b>Instant</b> Results</div>
        <div class="pill">🔄 <b>Reversible</b> Redaction</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["  🔒  Redact Data  ", "  🔓  Restore Data  "])

# ═══════════════════════════════════════════════════════════
# TAB 1
# ═══════════════════════════════════════════════════════════
with tab1:

    st.markdown("""
    <div class="steps-row">
        <div class="step"><div class="step-n">01</div><div class="step-t">Upload Document</div><div class="step-s">Any TXT, PDF, DOCX or CSV file</div></div>
        <div class="step"><div class="step-n">02</div><div class="step-t">Scan & Redact</div><div class="step-s">AI finds all sensitive data instantly</div></div>
        <div class="step"><div class="step-n">03</div><div class="step-t">Download Safe File</div><div class="step-s">Share without any privacy risk</div></div>
        <div class="step"><div class="step-n">04</div><div class="step-t">Save Mapping</div><div class="step-s">Restore original data anytime</div></div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Drop your file here — TXT, PDF, DOCX, CSV supported", type=["txt","pdf","docx","csv"])

    sample = """Patient Record - City Hospital
Name: Rahul Sharma
DOB: 15/08/1995
Aadhaar: 1234 5678 9012
Phone: +91 9876543210
Email: rahul.sharma@gmail.com
Password: rahul@1995
Address: Flat 4B, Green Valley Apartments, Hyderabad - 500032
Diagnosis: Type 2 Diabetes
Prescribed by: Dr. Priya Mehta
Bank Account: 9876543210123456"""

    file_content = ""
    if uploaded_file:
        with st.spinner(f"Reading {uploaded_file.name}..."):
            file_content = read_file(uploaded_file)
            if "ERROR:" in file_content:
                st.error(f"❌ Missing library. Run: pip3 install {file_content.split(':')[1]}")
                file_content = ""
            else:
                st.success(f"✅ **{uploaded_file.name}** loaded — {len(file_content):,} characters")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="slabel"><span class="dot-red"></span>Original Document — Unsafe</div>', unsafe_allow_html=True)
        input_text = st.text_area("", value=file_content or sample, height=260, label_visibility="collapsed", key="inp1")
        scan_btn = st.button("🔍  Scan & Redact PII", use_container_width=True)

    with col2:
        st.markdown('<div class="slabel"><span class="dot-green"></span>Redacted Document — Safe to Share</div>', unsafe_allow_html=True)
        rph = st.empty()
        rph.markdown('<div class="out-placeholder">🔒<br><br>Redacted document will appear here<br><span style="font-size:11px;">Click Scan & Redact to begin</span></div>', unsafe_allow_html=True)

    if scan_btn:
        if not input_text.strip():
            st.error("⚠️ Please upload a file or enter some text.")
        elif not api_key:
            st.error("❌ API key missing. Add GROQ_API_KEY to your .env file.")
        else:
            with st.spinner("Scanning for sensitive data..."):
                try:
                    client = Groq(api_key=api_key)
                    prompt = f"""You are a PII detection expert.

ONLY detect these 7 PII types:
1. Name  2. DOB  3. Phone Number  4. Email  5. Password  6. Aadhaar Number  7. Bank Account Number

For each found, return type and original value.
Create token mapping: [NAME_1], [PHONE_1], [EMAIL_1], [AADHAAR_1], [DOB_1], [PASSWORD_1], [BANK_1]

Masking rules for redacted_text:
- Name → XXXXX XXXXX
- DOB → XX/XX/XXXX
- Phone → XXXXXXXXXX
- Email → XXXXX@XXXXX.XXX
- Password → XXXXXXXX
- Aadhaar → show first 4 digits then XXXX XXXX (e.g. 1234 XXXX XXXX)
- Bank Account → show first 6 digits then X for rest (e.g. 987654XXXXXXXXXX)

DO NOT redact address or anything else.

Return ONLY this JSON:
{{
  "risk_score": <1-10>,
  "risk_level": "<HIGH/MEDIUM/LOW>",
  "pii_mapping": {{ "[NAME_1]": "original" }},
  "pii_found": [{{"type": "", "value": "", "masked": ""}}],
  "redacted_text": "<full text with only 7 types masked>",
  "summary": "<one sentence>"
}}

Text:
{input_text}

ONLY return valid JSON."""

                    resp = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role":"user","content":prompt}],
                        temperature=0.1
                    )
                    raw = resp.choices[0].message.content.strip()
                    raw = re.sub(r"```json\s*","",raw); raw = re.sub(r"```\s*","",raw)
                    result = json.loads(raw)

                    pii_list = result.get("pii_found",[])
                    redacted = input_text
                    for item in pii_list:
                        orig = item.get("value","")
                        sm = smart_mask(item.get("type",""), orig)
                        if sm:
                            item["masked"] = sm
                            redacted = redacted.replace(orig, sm)

                    st.session_state.pii_mapping = result.get("pii_mapping",{})
                    st.session_state.redacted_text = redacted

                    rph.markdown(f'<div class="out-safe">{redacted}</div>', unsafe_allow_html=True)

                    # Metrics
                    score = result.get("risk_score",0)
                    level = result.get("risk_level","LOW").upper()
                    cls = level.lower() if level in ["HIGH","MEDIUM","LOW"] else "neutral"
                    pii_count = len(pii_list)

                    st.markdown(f"""
                    <div class="metrics-row">
                        <div class="metric-card {cls}">
                            <div class="m-label">Risk Score</div>
                            <div class="m-val-{cls}">{score}<span style="font-size:16px;font-weight:400;">/10</span></div>
                        </div>
                        <div class="metric-card {cls}">
                            <div class="m-label">Risk Level</div>
                            <div class="m-val-{cls}">{level}</div>
                        </div>
                        <div class="metric-card neutral">
                            <div class="m-label">PII Found</div>
                            <div class="m-val-neutral">{pii_count}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # PII Table
                    st.markdown("**🔍 Detected PII**")
                    if pii_list:
                        rows = ""
                        for item in pii_list:
                            rows += f"""<tr>
                                <td><span class="chip chip-type">{item.get('type','')}</span></td>
                                <td><span class="chip chip-orig">{item.get('value','')}</span></td>
                                <td><span class="chip chip-mask">{item.get('masked','XXXXX')}</span></td>
                            </tr>"""
                        st.markdown(f"""
                        <div class="pii-wrap">
                        <table class="pii-table">
                            <thead><tr>
                                <th>PII Type</th>
                                <th>Original Value</th>
                                <th>Masked As</th>
                            </tr></thead>
                            <tbody>{rows}</tbody>
                        </table>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                    st.markdown("**📋 Summary**")
                    st.markdown(f'<div class="summary-card">{result.get("summary","")}</div>', unsafe_allow_html=True)

                    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                    st.markdown("**📥 Download Files**")
                    d1, d2 = st.columns(2)
                    with d1:
                        st.download_button("⬇️  Download Redacted Document", data=redacted, file_name="redacted_document.txt", mime="text/plain", use_container_width=True)
                    with d2:
                        st.download_button("🗝️  Download Token Mapping", data=json.dumps(st.session_state.pii_mapping, indent=2), file_name="pii_mapping.json", mime="application/json", use_container_width=True)

                    st.success("✅ Done! Switch to the 🔓 Restore tab to get the original data back.")

                except json.JSONDecodeError:
                    st.error("❌ Parsing failed. Please try again.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ═══════════════════════════════════════════════════════════
# TAB 2
# ═══════════════════════════════════════════════════════════
with tab2:

    st.markdown("""
    <div class="steps-row">
        <div class="step"><div class="step-n">01</div><div class="step-t">Paste Redacted Text</div><div class="step-s">The document with masked values</div></div>
        <div class="step"><div class="step-n">02</div><div class="step-t">Upload Mapping File</div><div class="step-s">The secret pii_mapping.json</div></div>
        <div class="step"><div class="step-n">03</div><div class="step-t">Restore Original</div><div class="step-s">Get the full original document back</div></div>
    </div>
    """, unsafe_allow_html=True)

    col3, col4 = st.columns(2, gap="large")

    with col3:
        st.markdown('<div class="slabel"><span class="dot-green"></span>Redacted Document</div>', unsafe_allow_html=True)
        redacted_input = st.text_area("", value=st.session_state.redacted_text or "", height=220, label_visibility="collapsed", key="ri")

        st.markdown('<div class="slabel" style="margin-top:16px;"><span class="dot-blue"></span>Token Mapping (JSON)</div>', unsafe_allow_html=True)
        default_map = json.dumps(st.session_state.pii_mapping, indent=2) if st.session_state.pii_mapping else '{\n  "[NAME_1]": "Rahul Sharma"\n}'
        mapping_input = st.text_area("", value=default_map, height=160, label_visibility="collapsed", key="mi")

        up_map = st.file_uploader("Or upload pii_mapping.json", type=["json"], key="mu")
        if up_map:
            mapping_input = up_map.read().decode("utf-8")
            st.success("✅ Mapping file loaded!")

        restore_btn = st.button("🔓  Restore Original Data", use_container_width=True)

    with col4:
        st.markdown('<div class="slabel"><span class="dot-blue"></span>Restored Document — Original Data</div>', unsafe_allow_html=True)
        rph2 = st.empty()
        rph2.markdown('<div class="out-placeholder">🔓<br><br>Restored document will appear here<br><span style="font-size:11px;">Click Restore Original Data to begin</span></div>', unsafe_allow_html=True)

    if restore_btn:
        try:
            mapping = json.loads(mapping_input)
            restored = redacted_input
            for token, original in mapping.items():
                restored = restored.replace(token, original)

            rph2.markdown(f'<div class="out-restored">{restored}</div>', unsafe_allow_html=True)

            count = sum(1 for t in mapping if t in redacted_input)
            st.markdown(f"""
            <div class="metrics-row">
                <div class="metric-card neutral">
                    <div class="m-label">Values Restored</div>
                    <div class="m-val-neutral">{count}</div>
                </div>
                <div class="metric-card low">
                    <div class="m-label">Status</div>
                    <div class="m-val-low" style="font-size:20px;padding-top:5px;">Complete ✓</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.download_button("⬇️  Download Restored Document", data=restored, file_name="restored_document.txt", mime="text/plain", use_container_width=True)
            st.success("✅ Original data successfully restored!")

            with st.expander("👁️ Side-by-Side Comparison"):
                e1, e2 = st.columns(2)
                with e1:
                    st.markdown('<div class="slabel"><span class="dot-green"></span>Redacted</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="out-safe" style="min-height:160px;">{redacted_input}</div>', unsafe_allow_html=True)
                with e2:
                    st.markdown('<div class="slabel"><span class="dot-blue"></span>Restored</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="out-restored" style="min-height:160px;">{restored}</div>', unsafe_allow_html=True)

        except json.JSONDecodeError:
            st.error("❌ Invalid JSON. Please check the mapping format.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown('<div style="text-align:center;padding:32px 0 16px;font-size:12px;color:var(--text-muted);">🛡️ ShieldPII · KLH Hack with AI 2026 · Privacy & Compliance Automation · Problem #61</div>', unsafe_allow_html=True)
