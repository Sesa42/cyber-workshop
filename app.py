import streamlit as st
import time
import random
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Cyber Resilience Mega Sandbox",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# auto refresh ogni secondo
st_autorefresh(interval=1000, key="timer")

# -----------------------------
# CSS STYLE
# -----------------------------
st.markdown("""
<style>
:root {
--win11-radius:14px;
--win11-border:rgba(255,255,255,0.18);
--win11-acrylic:rgba(18,18,20,0.52);
--win11-text:#f5f7fb;
--win11-accent:#0078d4;
}
.stApp {
background:url("https://4kwallpapers.com/images/wallpapers/windows-11-stock-official-blue-background-3840x2160-5630.jpg");
background-size:cover;
background-attachment:fixed;
}
[data-testid="stAppViewContainer"] > .main {
background: var(--win11-acrylic);
backdrop-filter: blur(18px) saturate(175%);
}
.stMarkdown, label, p, h1, h2, h3 { color: var(--win11-text) !important; }

.content-container {
background: rgba(255,255,255,0.95) !important;
padding: 40px;
border-radius: var(--win11-radius);
color: #141414 !important;
}
.content-container * { color: #141414 !important; }

.stButton>button {
background-color: var(--win11-accent) !important;
color: white !important;
width: 100%;
}
.status-panel {
background: rgba(0, 0, 0, 0.6) !important;
padding: 15px;
border-radius: var(--win11-radius);
text-align: center;
border: 1px solid var(--win11-border);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "resilience" not in st.session_state:
    st.session_state.resilience = 100
if "hacked" not in st.session_state:
    st.session_state.hacked = False
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "logs" not in st.session_state:
    st.session_state.logs = []

# -----------------------------
# TIMER IN SYNC
# -----------------------------
if "remaining" not in st.session_state:
    st.session_state.remaining = 180
if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

# Aggiorniamo timer solo se passa almeno 1 secondo
now = time.time()
delta = now - st.session_state.last_update
if delta >= 1:
    st.session_state.remaining = max(0, st.session_state.remaining - int(delta))
    st.session_state.last_update = now

remaining = st.session_state.remaining
attack_progress = int((180 - remaining)/180 * 100)
if remaining == 0:
    st.session_state.hacked = True

# -----------------------------
# RANDOM EVENTS
# -----------------------------
if random.random() < 0.02:
    st.session_state.logs.append("⚠️ Suspicious outbound network traffic detected")

# -----------------------------
# HEADER
# -----------------------------
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="status-panel"><h3>⏳ TIME: {remaining}s</h3></div>', unsafe_allow_html=True)
with col2:
    score = st.session_state.resilience
    color = "#00ff00" if score > 50 else "#ff4b4b"
    st.markdown(f'<div class="status-panel"><h3>🛡️ RESILIENCE: <span style="color:{color};">{score}%</span></h3></div>', unsafe_allow_html=True)

st.write("### 🔐 Encryption Activity")
st.progress(attack_progress)

# -----------------------------
# HACKED SCREEN
# -----------------------------
if st.session_state.hacked:
    st.markdown(
        '<div style="background-color:#a80000; padding:100px; border-radius:15px; text-align:center;">'
        '<h1 style="color:white !important;">🚨 SYSTEM BREACH 🚨</h1>'
        '<p style="color:white !important;">Ransomware encryption complete.</p></div>',
        unsafe_allow_html=True
    )
    st.write("## Incident Report")
    if score > 80:
        st.success("Excellent cyber awareness")
    elif score > 50:
        st.warning("Moderate cyber awareness")
    else:
        st.error("High risk behaviour detected")
    st.metric("Final Security Score", f"{score}%")
    if st.button("RESTART SYSTEM"):
        st.session_state.resilience = 100
        st.session_state.hacked = False
        st.session_state.start_time = time.time()
        st.session_state.remaining = 180
        st.session_state.last_update = time.time()
        st.session_state.logs = []
    st.stop()

# -----------------------------
# APPLICATION SELECTOR
# -----------------------------
app = st.selectbox(
    "Select Application:",
    ["📧 Outlook Mail", "💬 Teams Chat", "📂 OneDrive Audit", "🛡️ Defender", "⚙️ Settings",
     "📊 Dashboard Analytics", "🔑 MFA Simulator", "🖥 Remote Desktop", "💣 Fake Virus Scan",
     "📁 File Recovery", "📡 Network Monitor", "🛒 Fake Email Shop", "🎯 Cyber Quiz"],
    label_visibility="collapsed"
)

st.markdown('<div class="content-container">', unsafe_allow_html=True)

# -----------------------------
# Moduli classici + extra
# -----------------------------
# (qui andrebbero messi tutti i moduli come nell’ultima versione)
# L’unica differenza è che **non usiamo più st.rerun() nei pulsanti**, solo aggiornamento session_state
# es.:
if app == "📧 Outlook Mail":
    st.write("## 📧 Outlook Web")
    st.info("Incoming: 'Urgent: Payment Declined' from security@microsoft-office.net")
    c1, c2 = st.columns(2)
    if c1.button("Verify Now"):
        st.session_state.resilience = max(0, st.session_state.resilience - 40)
        st.session_state.logs.append("❌ PHISHED! User clicked phishing link")
        st.error("Credential harvesting page opened")
    if c2.button("Report Phishing"):
        st.session_state.resilience = min(100, st.session_state.resilience + 20)
        st.session_state.logs.append("✔ Phishing email reported")
        st.success("Threat reported to SOC")

# ... (aggiungi tutti gli altri moduli seguendo lo stesso schema)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# SOC LOG
# -----------------------------
st.write("### 📜 Security Log")
for log in reversed(st.session_state.logs[-6:]):
    st.write("•", log)
