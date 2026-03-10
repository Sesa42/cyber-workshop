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
# TIMER & RANSOMWARE PROGRESS
# -----------------------------
elapsed = time.time() - st.session_state.start_time
remaining = max(0, int(180 - elapsed))
attack_progress = int((elapsed / 180) * 100)
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

# -----------------------------
# ENCRYPTION PROGRESS
# -----------------------------
st.write("### 🔐 Encryption Activity")
st.progress(min(attack_progress, 100))

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
        st.session_state.logs = []
        st.rerun()
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
# OUTLOOK PHISHING
# -----------------------------
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

# -----------------------------
# TEAMS SOCIAL ENGINEERING
# -----------------------------
elif app == "💬 Teams Chat":
    st.write("## 💬 Microsoft Teams")
    st.markdown(
        '<div style="background:#f3f2f1; padding:15px; border-left:5px solid #6264a7; border-radius:10px;">'
        '<b>Mark (IT Support):</b> Hi! Send me the MFA code you just received to verify your login.</div>',
        unsafe_allow_html=True
    )
    ca, cb = st.columns(2)
    if ca.button("Send Code"):
        st.session_state.hacked = True
        st.session_state.logs.append("🚨 MFA code shared with attacker")
        st.rerun()
    if cb.button("Report User"):
        st.session_state.resilience = min(100, st.session_state.resilience + 30)
        st.session_state.logs.append("🏆 Social engineering attempt reported")
        st.success("User reported to security team")

# -----------------------------
# ONEDRIVE AUDIT
# -----------------------------
elif app == "📂 OneDrive Audit":
    st.write("## 📂 OneDrive Audit")
    st.info("Detected unusual file download activity")
    c1, c2 = st.columns(2)
    if c1.button("Investigate Files"):
        st.session_state.resilience = max(0, st.session_state.resilience - 20)
        st.session_state.logs.append("❌ Unreviewed file access")
        st.error("Potential data exfiltration")
    if c2.button("Report Incident"):
        st.session_state.resilience = min(100, st.session_state.resilience + 25)
        st.session_state.logs.append("✔ File access incident reported")
        st.success("Incident reported to SOC")

# -----------------------------
# DEFENDER PANEL
# -----------------------------
elif app == "🛡️ Defender":
    st.write("## 🛡️ Microsoft Defender")
    st.warning("Suspicious PowerShell activity detected")
    if st.button("Isolate Device"):
        st.session_state.resilience = min(100, st.session_state.resilience + 15)
        st.session_state.logs.append("Endpoint isolated from network")
        st.success("Device isolated successfully")

# -----------------------------
# SETTINGS
# -----------------------------
elif app == "⚙️ Settings":
    st.write("## ⚙️ Settings")
    st.write("Adjust simulation parameters (future extension)")

# -----------------------------
# EXTRA FUN MODULES
# -----------------------------
elif app == "📊 Dashboard Analytics":
    st.write("## 📊 Dashboard Analytics")
    st.bar_chart({"Resilience":[st.session_state.resilience, 100-st.session_state.resilience]})

elif app == "🔑 MFA Simulator":
    st.write("## 🔑 MFA Simulator")
    if st.button("Attempt MFA Bypass"):
        st.session_state.hacked = True
        st.session_state.logs.append("🚨 MFA bypass attempt failed")

elif app == "🖥 Remote Desktop":
    st.write("## 🖥 Remote Desktop / VPN Alerts")
    st.warning("New VPN login from unknown location detected")
    if st.button("Block IP"):
        st.session_state.resilience = min(100, st.session_state.resilience + 10)
        st.success("IP blocked successfully")

elif app == "💣 Fake Virus Scan":
    st.write("## 💣 Fake Virus Scan")
    st.progress(random.randint(0,100))
    if st.button("Quarantine Threats"):
        st.session_state.resilience = min(100, st.session_state.resilience + 15)
        st.success("Fake threats neutralized")

elif app == "📁 File Recovery":
    st.write("## 📁 File Recovery")
    if st.button("Recover Critical Files"):
        st.session_state.resilience = min(100, st.session_state.resilience + 20)
        st.success("Files recovered successfully")

elif app == "📡 Network Monitor":
    st.write("## 📡 Network Monitor")
    st.line_chart({"Suspicious Packets":[random.randint(0,50) for _ in range(10)]})

elif app == "🛒 Fake Email Shop":
    st.write("## 🛒 Fake Email Shop")
    if st.button("Click Suspicious Link"):
        st.session_state.resilience = max(0, st.session_state.resilience - 30)
        st.error("Phishing link clicked!")

elif app == "🎯 Cyber Quiz":
    st.write("## 🎯 Cyber Quiz")
    q = "What is the safest way to handle unknown attachments?"
    answer = st.radio(q, ["Open immediately","Scan with antivirus","Forward to friend"])
    if st.button("Submit Answer"):
        if answer == "Scan with antivirus":
            st.success("Correct! Resilience increased")
            st.session_state.resilience = min(100, st.session_state.resilience + 20)
            st.session_state.logs.append("✔ Quiz correct answer")
        else:
            st.error("Incorrect! Resilience decreased")
            st.session_state.resilience = max(0, st.session_state.resilience - 10)
            st.session_state.logs.append("❌ Quiz wrong answer")

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# SOC LOG
# -----------------------------
st.write("### 📜 Security Log")
for log in reversed(st.session_state.logs[-6:]):
    st.write("•", log)
