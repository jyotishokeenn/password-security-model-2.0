import streamlit as st
import re
import math
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Password Security Advisor",
    page_icon="🔐",
    layout="wide"
)

# ---------------- IMAGE ----------------

st.image(
    "https://humanfocus.co.uk/wp-content/uploads/password-security-800x800.jpg",
    width=500
)

st.title("🔐 Password Security Advisor")
st.markdown("### Cybersecurity Toolkit with Gemini AI")

# ---------------- PASSWORD STRENGTH ----------------

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

# ---------------- ENTROPY ----------------

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

# ---------------- RISK ANALYZER ----------------

def risk_analyzer(password):
    risks = []

    common_passwords = [
        "password",
        "123456",
        "12345678",
        "qwerty",
        "admin",
        "welcome",
        "abc123"
    ]

    if password.lower() in common_passwords:
        risks.append("Common password detected")

    if re.search(r"(.)\1{2,}", password):
        risks.append("Repeated characters detected")

    patterns = [
        "1234", "2345", "3456",
        "4567", "5678", "6789",
        "abcd", "bcde", "cdef"
    ]

    for p in patterns:
        if p in password.lower():
            risks.append("Sequential pattern detected")
            break

    return risks

# ---------------- RECOMMENDATIONS ----------------

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

# ---------------- SECURITY SCORE ----------------

def security_score(score, entropy, risks):
    final = score * 15

    if entropy > 60:
        final += 20
    elif entropy > 40:
        final += 10

    final -= len(risks) * 10

    return max(0, min(100, final))

# ---------------- POLICY GENERATOR ----------------

def generate_password_policy(org_type, employees, security_level, api_key):

    try:

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
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

# ---------------- PHISHING DETECTOR ----------------

def detect_phishing(email_text):

    suspicious_words = [
        "urgent",
        "verify account",
        "click here",
        "free money",
        "winner",
        "bank account",
        "password reset",
        "limited time"
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

# ---------------- CYBER CHAT ----------------

def cyber_chat(question, api_key):

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-2.5-flash")

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

  prompt = f"..."

    response = model.generate_content(prompt)

    return response.text

except Exception as e:
    return f"Error: {e}"

# ---------------- FIR ----------------

def generate_fir(name, item, place):

    return f"""
LOST AND FOUND REPORT

Name: {name}

Lost Item: {item}

Place of Loss: {place}

I hereby report that the above-mentioned item has been lost.

Kindly register this complaint and assist in locating the item.

Signature:
{name}"""

# ---------------- TABS ----------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Password Analysis",
    "Policy Generator",
    "Phishing Detector",
    "Cyber Expert",
    "FIR Generator"
])

# ====================================================
# PASSWORD ANALYSIS
# ====================================================

with tab1:

    password = st.text_input(
        "Enter Password",
        type="password"
    )

    if st.button("Analyze Password"):

        if password:

            strength, score = password_strength(password)

            entropy = calculate_entropy(password)

            risks = risk_analyzer(password)

            recommendations = recommendation_engine(password)

            sec_score = security_score(
                score,
                entropy,
                risks
            )

            st.subheader("Security Report")

            c1, c2, c3 = st.columns(3)

            c1.metric("Strength", strength)
            c2.metric("Entropy", f"{entropy} bits")
            c3.metric("Score", f"{sec_score}/100")

            st.progress(sec_score / 100)

            st.subheader("Risks")

            if risks:
                for r in risks:
                    st.warning(r)
            else:
                st.success("No major risks detected.")

            st.subheader("Recommendations")

            if recommendations:
                for r in recommendations:
                    st.info(r)
            else:
                st.success("Excellent Password")

# ====================================================
# POLICY GENERATOR
# ====================================================

with tab2:

    st.subheader("Organization Password Policy Generator")

    org_type = st.text_input("Organization Type")

    employees = st.number_input(
        "Number of Employees",
        min_value=1
    )

    security_level = st.selectbox(
        "Security Level",
        ["Low", "Medium", "High"]
    )

    api_key = st.text_input(
        "Gemini API Key",
        type="password"
    )

    if st.button("Generate Policy"):

        policy = generate_password_policy(
            org_type,
            employees,
            security_level,
            api_key
        )

        st.markdown(policy)

        st.download_button(
            "📥 Download Policy",
            policy,
            file_name="Password_Policy.txt"
        )

# ====================================================
# PHISHING DETECTOR
# ====================================================

with tab3:

    st.subheader("📧 Email Phishing Detection")

    email_text = st.text_area(
        "Paste Email Content"
    )

    if st.button("Analyze Email"):

        result = detect_phishing(email_text)

        st.success(result)

# ====================================================
# CYBER EXPERT
# ====================================================

with tab4:

    st.subheader("🤖 Chat With Cyber Expert")

    chat_api = st.text_input(
        "Gemini API Key",
        type="password",
        key="chat_api"
    )

    question = st.text_area(
        "Ask Cyber Security Question"
    )

    if st.button("Ask Expert"):

        answer = cyber_chat(
            question,
            chat_api
        )

        st.write(answer)

# ====================================================
# FIR GENERATOR
# ====================================================

with tab5:

    st.subheader("📄 Lost & Found FIR Generator")

    name = st.text_input("Your Name")

    item = st.text_input("Lost Item")

    place = st.text_input("Place of Loss")

    if st.button("Generate FIR"):

        fir = generate_fir(
            name,
            item,
            place
        )

        st.text_area(
            "Generated FIR",
            fir,
            height=250
        )

        st.download_button(
            "📥 Download FIR",
            fir,
            file_name="FIR_Report.txt"
        )
