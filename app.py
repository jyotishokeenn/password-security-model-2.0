import streamlit as st
import re
import math
import google.generativeai as genai
import plotly.graph_objects as go

# PAGE CONFIG

st.set_page_config(
    page_title="SecureAccess // Password Intelligence Terminal",
    page_icon="🛡️",
    layout="wide"
)

# THEME — "Security Operations Console"

st.markdown("""
<style>

:root{
  --bg-primary:#EEF2F7;
  --bg-panel:#FFFFFF;
  --bg-panel-alt:#F8FAFC;

  --border-subtle:#CBD5E1;

  --accent-cyan:#2563EB;
  --accent-cyan-dark:#1D4ED8;

  --accent-amber:#D97706;
  --accent-red:#DC2626;

  --text-primary:#111827;
  --text-secondary:#374151;
  --text-muted:#6B7280;
}

html, body, [class*="css"]{
    font-family:'Inter', sans-serif;
    color:var(--text-primary);
}

.stApp{
    background:var(--bg-primary);
    color:var(--text-primary);
}

.block-container{
    padding-top:1.5rem;
    padding-bottom:2rem;
    max-width:1100px;
}

#MainMenu, footer, header{
    visibility:hidden;
}

/* STATUS BAR */

.status-bar{
    display:flex;
    justify-content:space-between;
    align-items:center;
    flex-wrap:wrap;
    gap:0.4rem;

    font-family:'JetBrains Mono', monospace;
    font-size:0.72rem;
    letter-spacing:0.08em;
    text-transform:uppercase;

    color:var(--text-secondary);

    border:1px solid var(--border-subtle);
    background:white;

    border-radius:10px;
    padding:0.7rem 1rem;
    margin-bottom:1.4rem;

    box-shadow:0 2px 8px rgba(0,0,0,0.04);
}

.status-dot{
    display:inline-block;
    width:8px;
    height:8px;
    border-radius:50%;
    background:#2563EB;
    margin-right:6px;
}

/* HERO */

.hero{
    border:1px solid var(--border-subtle);
    background:white;
    border-radius:16px;
    padding:2.2rem 2.4rem;
    margin-bottom:1.6rem;

    box-shadow:0 4px 12px rgba(15,23,42,0.05);
}

.hero-eyebrow{
    font-family:'JetBrains Mono', monospace;
    color:#2563EB;
    font-size:0.75rem;
    letter-spacing:0.18em;
    text-transform:uppercase;
}

.hero-title{
    font-family:'Space Grotesk', sans-serif;
    font-size:2.5rem;
    font-weight:700;
    color:#111827;
}

.hero-title span{
    color:#2563EB;
}

.hero-sub{
    color:#374151;
    font-size:1rem;
    line-height:1.6;
}

/* PANEL TITLE */

.panel-title{
    font-family:'JetBrains Mono', monospace;
    font-size:0.78rem;
    letter-spacing:0.1em;
    text-transform:uppercase;

    color:#1D4ED8;

    margin-bottom:0.9rem;
    border-bottom:1px solid #D1D5DB;
    padding-bottom:0.6rem;
    font-weight:700;
}

/* METRIC CARDS */

.metric-chip{
    border:1px solid #D1D5DB;
    background:white;
    border-radius:12px;
    padding:1rem;
    text-align:center;

    box-shadow:0 2px 8px rgba(0,0,0,0.04);
}

.metric-chip .val{
    font-family:'JetBrains Mono', monospace;
    font-size:1.6rem;
    font-weight:700;
    color:#111827;
}

.metric-chip .lbl{
    font-size:0.7rem;
    letter-spacing:0.09em;
    text-transform:uppercase;
    color:#6B7280;
}

/* ALERTS */

.alert-card{
    border-radius:10px;
    padding:0.8rem;
    margin-bottom:0.6rem;
    font-weight:500;
}

.alert-risk{
    background:#FEE2E2;
    color:#991B1B;
    border-left:4px solid #DC2626;
}

.alert-warn{
    background:#FEF3C7;
    color:#92400E;
    border-left:4px solid #D97706;
}

.alert-ok{
    background:#DCFCE7;
    color:#166534;
    border-left:4px solid #16A34A;
}

/* FIR CARD */

.doc-card{
    border:1px solid #D1D5DB;
    background:white;
    border-radius:12px;
    padding:1.4rem;
    font-family:'JetBrains Mono', monospace;
    color:#111827;
    white-space:pre-wrap;
}

/* TABS */

.stTabs [data-baseweb="tab"]{
    color:#111827;
    font-weight:600;
}

.stTabs [aria-selected="true"]{
    color:#2563EB !important;
    border-bottom:2px solid #2563EB !important;
}

/* CONTAINERS */

div[data-testid="stVerticalBlockBorderWrapper"]{
    background:white !important;
    border:1px solid #D1D5DB !important;
    border-radius:14px !important;

    box-shadow:0 4px 12px rgba(15,23,42,0.05);
}

/* INPUTS */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
div[data-baseweb="select"] > div{
    background:white !important;
    color:#111827 !important;
    border:1px solid #CBD5E1 !important;
    border-radius:8px !important;
}

/* BUTTONS */

.stButton > button{
    background:#2563EB;
    color:white;
    border:none;
    border-radius:10px;
    font-weight:600;
    transition:all .2s ease;
}

.stButton > button:hover{
    background:#1D4ED8;
    color:white;
    transform:translateY(-1px);
}

/* DOWNLOAD BUTTON */

.stDownloadButton > button{
    background:white;
    color:#2563EB;
    border:1px solid #2563EB;
    border-radius:10px;
    font-weight:600;
}

/* PROGRESS BAR */

div[data-testid="stProgress"] > div > div{
    background:#2563EB !important;
    border-radius:10px;
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
    background:#F8FAFC;
}

section[data-testid="stSidebar"] *{
    color:#111827 !important;
}

/* FOOTER */

.app-footer{
    text-align:center;
    font-family:'JetBrains Mono', monospace;
    font-size:0.75rem;
    color:#6B7280;
    margin-top:2rem;
}

</style>
""", unsafe_allow_html=True)

# LOGIC — unchanged from the working version

def password_strength(password):
    score = 0

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"[a-z]", password):
        score += 1

    if re.search(r"\d", password):
        score += 1

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    if score <= 2:
        return "Weak", score
    elif score <= 4:
        return "Medium", score
    elif score == 5:
        return "Strong", score
    else:
        return "Very Strong", score


def calculate_entropy(password):
    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26

    if re.search(r"[A-Z]", password):
        charset += 26

    if re.search(r"\d", password):
        charset += 10

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        charset += 32

    if charset == 0:
        return 0

    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)


def risk_analyzer(password):
    risks = []

    common_passwords = [
        "password", "123456", "12345678", "qwerty",
        "admin", "welcome", "abc123"
    ]

    if password.lower() in common_passwords:
        risks.append("Common password detected")

    if re.search(r"(.)\1{2,}", password):
        risks.append("Repeated characters detected")

    patterns = [
        "1234", "2345", "3456", "4567", "5678", "6789",
        "abcd", "bcde", "cdef"
    ]

    for p in patterns:
        if p in password.lower():
            risks.append("Sequential pattern detected")
            break

    return risks


def recommendation_engine(password):
    rec = []

    if len(password) < 12:
        rec.append("Use at least 12 characters")

    if not re.search(r"[A-Z]", password):
        rec.append("Add uppercase letters")

    if not re.search(r"[a-z]", password):
        rec.append("Add lowercase letters")

    if not re.search(r"\d", password):
        rec.append("Add numbers")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        rec.append("Add special characters")

    return rec


def security_score(score, entropy, risks):
    final = score * 15

    if entropy > 60:
        final += 20
    elif entropy > 40:
        final += 10

    final -= len(risks) * 10

    return max(0, min(100, final))


def generate_password_policy(org_type, employees, security_level, api_key):
    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            "gemini-3.5-flash-lite"
        )

        prompt = f"""
Generate a professional password security policy.

Organization Type: {org_type}
Employees: {employees}
Security Level: {security_level}

Include:
1. Password Length
2. Complexity Requirements
3. Password Expiry
4. Password History
5. Multi-Factor Authentication
6. Account Lockout Rules
7. Security Best Practices

Format professionally.
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error: {e}"


def detect_phishing(email_text):
    suspicious_words = [
        "urgent", "verify account", "click here", "free money",
        "winner", "bank account", "password reset", "limited time"
    ]

    score = 0

    for word in suspicious_words:
        if word.lower() in email_text.lower():
            score += 1

    if score >= 3:
        return "🚨 High Risk Phishing Email"
    elif score >= 1:
        return "⚠ Suspicious Email"
    else:
        return "✅ Safe Email"


def cyber_chat(question, api_key):
    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-3.5-flash-lite")

        prompt = f"""
You are a Cyber Security Expert.

Answer the following cybersecurity question in a clear and professional manner.

Question:
{question}
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error: {e}"


def generate_fir(name, item, place):
    return f"""LOST AND FOUND REPORT

Name: {name}

Lost Item: {item}

Place of Loss: {place}

I hereby report that the above-mentioned item has been lost.

Kindly register this complaint and assist in locating the item.

Signature:
{name}"""

# UI HELPERS

def alert(text, kind="risk", icon=None):
    icons = {"risk": "✕", "warn": "!", "ok": "✓"}
    st.markdown(
        f'<div class="alert-card alert-{kind}">'
        f'<span class="alert-icon">{icon or icons.get(kind, "•")}</span>'
        f'<span>{text}</span></div>',
        unsafe_allow_html=True
    )


def metric_chip(col, value, label):
    col.markdown(
        f'<div class="metric-chip"><div class="val">{value}</div>'
        f'<div class="lbl">{label}</div></div>',
        unsafe_allow_html=True
    )


def gauge_color(score):
    if score < 40:
        return "#FF5470"
    elif score < 70:
        return "#FFB84D"
    return "#2DE1C2"


def render_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": " /100", "font": {"size": 34, "color": "#E7EDF3", "family": "JetBrains Mono"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#3A4A5A", "tickfont": {"color": "#8FA3B8", "size": 10}},
            "bar": {"color": gauge_color(score), "thickness": 0.28},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "rgba(255,84,112,0.12)"},
                {"range": [40, 70], "color": "rgba(255,184,77,0.12)"},
                {"range": [70, 100], "color": "rgba(45,225,194,0.12)"},
            ],
            "threshold": {"line": {"color": "#E7EDF3", "width": 2}, "thickness": 0.8, "value": score},
        }
    ))
    fig.update_layout(
        height=230,
        margin=dict(l=20, r=20, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#E7EDF3", "family": "Inter"}
    )
    return fig

# SIDEBAR

with st.sidebar:
    st.markdown(
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:1.3rem;'
        'font-weight:700;color:#E7EDF3;margin-bottom:0.2rem;">🛡️ SecureAccess</div>'
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.7rem;'
        'color:#2DE1C2;letter-spacing:0.1em;margin-bottom:1.2rem;">CYBERSECURITY TOOLKIT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-title">Console Status</div>'
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.78rem;'
        'color:#8FA3B8;line-height:2;">'
        '<span class="status-dot"></span>AI Engine — Gemini 2.5 Flash<br>'
        '<span class="status-dot"></span>Session — Local, not stored<br>'
        '<span class="status-dot"></span>Modules — 5 active'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()
    st.caption("Gemini API keys are used only for this session and are never stored or logged.")

# STATUS BAR + HERO

st.markdown(
    '<div class="status-bar">'
    '<div><span class="status-dot"></span>SYSTEM ONLINE</div>'
    '<div>MODULES: PASSWORD · POLICY · PHISHING · EXPERT · FIR</div>'
    '<div>ENCRYPTION: LOCAL SESSION</div>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero">'
    '<div class="hero-eyebrow">Cybersecurity Toolkit · Gemini AI</div>'
    '<div class="hero-title">Password <span>Intelligence</span> Terminal</div>'
    '<div class="hero-sub">Analyze password strength, generate organizational policies, '
    'detect phishing attempts, consult an AI cyber expert, and file lost-item reports — '
    'all from one console.</div>'
    '</div>',
    unsafe_allow_html=True
)

# TABS

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔑  Password Analysis",
    "📋  Policy Generator",
    "📧  Phishing Detector",
    "🤖  Cyber Expert",
    "📄  FIR Generator"
])

# PASSWORD ANALYSIS

with tab1:
    with st.container(border=True):
        st.markdown('<div class="panel-title">Input</div>', unsafe_allow_html=True)
        password = st.text_input("Enter Password", type="password", label_visibility="collapsed",
                                  placeholder="Enter a password to analyze")
        run = st.button("Analyze Password")

    if run:
        if password:
            strength, score = password_strength(password)
            entropy = calculate_entropy(password)
            risks = risk_analyzer(password)
            recommendations = recommendation_engine(password)
            sec_score = security_score(score, entropy, risks)

            gcol, mcol = st.columns([1.1, 1])

            with gcol:
                with st.container(border=True):
                    st.markdown('<div class="panel-title">Security Score</div>', unsafe_allow_html=True)
                    st.plotly_chart(render_gauge(sec_score), use_container_width=True, config={"displayModeBar": False})

            with mcol:
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                metric_chip(c1, strength, "Strength")
                metric_chip(c2, f"{entropy}", "Entropy (bits)")
                st.markdown("<br>", unsafe_allow_html=True)
                st.progress(sec_score / 100)

            rcol1, rcol2 = st.columns(2)

            with rcol1:
                with st.container(border=True):
                    st.markdown('<div class="panel-title">Risks Detected</div>', unsafe_allow_html=True)
                    if risks:
                        for r in risks:
                            alert(r, kind="risk")
                    else:
                        alert("No major risks detected.", kind="ok")

            with rcol2:
                with st.container(border=True):
                    st.markdown('<div class="panel-title">Recommendations</div>', unsafe_allow_html=True)
                    if recommendations:
                        for r in recommendations:
                            alert(r, kind="warn")
                    else:
                        alert("Excellent password — no changes needed.", kind="ok")
        else:
            st.warning("Enter a password first.")


# POLICY GENERATOR

with tab2:
    with st.container(border=True):
        st.markdown('<div class="panel-title">Organization Details</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        org_type = c1.text_input("Organization Type")
        employees = c2.number_input("Number of Employees", min_value=1)

        c3, c4 = st.columns(2)
        security_level = c3.selectbox("Security Level", ["Low", "Medium", "High"])
        api_key = c4.text_input("Gemini API Key", type="password")

        gen = st.button("Generate Policy")

    if gen:
        policy = generate_password_policy(org_type, employees, security_level, api_key)
        with st.container(border=True):
            st.markdown('<div class="panel-title">Generated Policy</div>', unsafe_allow_html=True)
            st.markdown(policy)
            st.download_button("📥 Download Policy", policy, file_name="Password_Policy.txt")


# PHISHING DETECTOR

with tab3:
    with st.container(border=True):
        st.markdown('<div class="panel-title">Email Content</div>', unsafe_allow_html=True)
        email_text = st.text_area("Paste Email Content", label_visibility="collapsed",
                                   placeholder="Paste the full email text here...", height=180)
        scan = st.button("Analyze Email")

    if scan:
        result = detect_phishing(email_text)
        kind = "ok" if "Safe" in result else ("risk" if "High Risk" in result else "warn")
        with st.container(border=True):
            st.markdown('<div class="panel-title">Scan Result</div>', unsafe_allow_html=True)
            alert(result, kind=kind, icon="🔍")

# CYBER EXPERT

with tab4:
    with st.container(border=True):
        st.markdown('<div class="panel-title">Ask a Question</div>', unsafe_allow_html=True)
        chat_api = st.text_input("Gemini API Key", type="password", key="chat_api")
        question = st.text_area("Ask Cyber Security Question", height=140)
        ask = st.button("Ask Expert")

    if ask:
        answer = cyber_chat(question, chat_api)
        with st.container(border=True):
            st.markdown('<div class="panel-title">Expert Answer</div>', unsafe_allow_html=True)
            st.write(answer)

# FIR GENERATOR

with tab5:
    with st.container(border=True):
        st.markdown('<div class="panel-title">Report Details</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        name = c1.text_input("Your Name")
        item = c2.text_input("Lost Item")
        place = c3.text_input("Place of Loss")
        make = st.button("Generate FIR")

    if make:
        fir = generate_fir(name, item, place)
        with st.container(border=True):
            st.markdown('<div class="panel-title">Generated Report</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="doc-card">{fir}</div>', unsafe_allow_html=True)
            st.download_button("📥 Download FIR", fir, file_name="FIR_Report.txt")


# FOOTER

st.markdown(
    '<div class="app-footer">SECUREACCESS TERMINAL · POWERED BY GEMINI AI · '
    'ALL ANALYSIS RUNS LOCALLY IN YOUR SESSION</div>',
    unsafe_allow_html=True
)
