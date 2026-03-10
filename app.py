```python
import streamlit as st
import time
import random

st.set_page_config(
    page_title="Cyber Resilience Sandbox",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------
# CSS STYLE (Windows 11 look)
# -------------------------
st.markdown(
"""
<style>

:root {
    --win11-radius:14px;
    --win11-border:rgba(255,255,255,0.18);
    --win11-acrylic:rgba(18,18,20,0.55);
    --win11-text:#f5f7fb;
    --win11-accent:#0078d4;
}

.stApp {
background:url("https://4kwallpapers.com/images/wallpapers/windows-11-stock-official-blue-background-3840x2160-5630.jpg");
background-size:cover;
background-attachment:fixed;
}

[data-testid="stAppViewContainer"] > .main {
background:var(--win11-acrylic);
backdrop-filter:blur(18px) saturate(160%);
}

.stMarkdown, label, p, h1, h2, h3 {
color:var(--win11-text)!important;
}

.content-container {
background:rgba(255,255,255,0.95)!important;
padding:40px;
border-radius:14px;
color:#141414!important;
}

.content-container * {
color:#141414!important;
}

.status-panel {
background:rgba(0,0,0,0.55);
padding:15px;
border-radius:14px;
text-align:center;
border:1px solid var(--win11-border);
}

.stButton>button{
background-color:var(--win11-accent)!important;
color:white!important;
width:100%;
}

</style>
""",
unsafe_allow_html=True
)

# -------------------------
# SESSION STATE
# -------------------------
if "resilience" not in st.session_state:
    st.session_state.resilience = 100

if "hacked" not in st.session_state:
    st.session_state.hacked = False

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "logs" not in st.session_state:
    st.session_state.logs = []

# -------------------------
# TIMER
# -------------------------
elapsed = time.time() - st.session_state.start_time
remaining = max(0, int(180 - elapsed))

if remaining == 0:
    st.session_state.hacked = True

# ransomware progress
attack_progress = int((elapsed / 180) * 100)

# -------------------------
# RANDOM EVENTS
# -------------------------
if random.random() < 0.02:
    st.session_state.logs.append("⚠️ Suspicious outbound network traffic")

# -------------------------
# HEADER STATUS
# -------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f'<div class="status-panel"><h3>⏳ TIME: {remaining}s</h3></div>',
        unsafe_allow_html=True
    )

with col2:

    score = st.session_state.resilience

    if score > 70:
        color = "#00ff88"
    elif score > 40:
        color = "#ffcc00"
    else:
        color = "#ff4b4b"

    st.markdown(
        f'<div class="status-panel"><h3>🛡️ RESILIENCE: <span style="color:{color};">{score}%</span></h3></div>',
        unsafe_allow_html=True
    )

# -------------------------
# RANSOMWARE PROGRESS
# -------------------------
st.write("### 🔐 Encryption Activity")
st.progress(min(attack_progress,100))

# -------------------------
# RANSOMWARE SCREEN
# -------------------------
if st.session_state.hacked:

    st.markdown(
    """
    <div style="background:#a80000;padding:80px;border-radius:15px;text-align:center">
    <h1 style="color:white!important;">🚨 SYSTEM BREACH 🚨</h1>
    <p style="color:white!important;">Ransomware encryption complete.</p>
    </div>
    """,
    unsafe_allow_html=True
    )

    st.write("## Incident Report")

    score = st.session_state.resilience

    if score > 80:
        st.success("Excellent cyber awareness")
    elif score > 50:
        st.warning("Moderate cyber awareness")
    else:
        st.error("High risk behaviour detected")

    st.metric("Final Security Score", f"{score}%")

    if st.button("🔁 RESTART SYSTEM"):
        st.session_state.resilience = 100
        st.session_state.hacked = False
        st.session_state.start_time = time.time()
        st.session_state.logs = []
        st.rerun()

    st.stop()

# -------------------------
# APP SELECTOR
# -------------------------
app = st.selectbox(
"Select Application",
["📧 Outlook Mail","💬 Teams Chat","🛡️ Defender"],
label_visibility="collapsed"
)

st.markdown('<div class="content-container">', unsafe_allow_html=True)

# -------------------------
# OUTLOOK PHISHING
# -------------------------
if app == "📧 Outlook Mail":

    st.write("## 📧 Outlook Web")

    st.info("Incoming: 'Urgent: Payment Declined' from security@microsoft-office.net")

    c1, c2 = st.columns(2)

    if c1.button("Verify Now"):

        st.session_state.resilience = max(0, st.session_state.resilience - 40)

        st.session_state.logs.append(
        "❌ User clicked phishing link"
        )

        st.error("Phishing site triggered credential harvest")

    if c2.button("Report Phishing"):

        st.session_state.resilience = min(100, st.session_state.resilience + 20)

        st.session_state.logs.append(
        "✔️ Phishing email reported"
        )

        st.success("Threat reported to SOC")

# -------------------------
# TEAMS SOCIAL ENGINEERING
# -------------------------
elif app == "💬 Teams Chat":

    st.write("## 💬 Microsoft Teams")

    st.markdown(
    """
    <div style="background:#f3f2f1;padding:15px;border-left:5px solid #6264a7;border-radius:10px;">
    <b>Mark (IT Support)</b><br>
    Hi! Send me the MFA code you just received to verify your login.
    </div>
    """,
    unsafe_allow_html=True
    )

    a,b = st.columns(2)

    if a.button("Send Code"):

        st.session_state.logs.append(
        "🚨 MFA code shared with attacker"
        )

        st.session_state.hacked = True
        st.rerun()

    if b.button("Report User"):

        st.session_state.resilience = min(100, st.session_state.resilience + 30)

        st.session_state.logs.append(
        "✔️ Social engineering attempt reported"
        )

        st.success("User reported to security team")

# -------------------------
# DEFENDER PANEL
# -------------------------
elif app == "🛡️ Defender":

    st.write("## 🛡️ Microsoft Defender")

    st.warning("Suspicious PowerShell activity detected")

    if st.button("Isolate Device"):

        st.session_state.resilience = min(100, st.session_state.resilience + 15)

        st.session_state.logs.append(
        "Endpoint isolated from network"
        )

        st.success("Device isolated successfully")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# SOC LOG
# -------------------------
st.write("### 📜 Security Log")

for log in reversed(st.session_state.logs[-6:]):
    st.write("•", log)

# -------------------------
# AUTO REFRESH
# -------------------------
time.sleep(1)
st.rerun()
