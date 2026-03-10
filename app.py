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

# Auto refresh ogni secondo per il timer
st_refresh_count = st_autorefresh(interval=1000, key="timer")

# -----------------------------
# CSS STYLE
# -----------------------------
st.markdown("""
<style>
    :root {
        --win11-radius: 14px;
        --win11-accent: #0078d4;
    }
    /* Sfondo globale */
    .stApp {
        background: url("https://4kwallpapers.com/images/wallpapers/windows-11-stock-official-blue-background-3840x2160-5630.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    /* Effetto vetro sul contenitore principale */
    [data-testid="stAppViewContainer"] > .main {
        background: rgba(18, 18, 20, 0.6);
        backdrop-filter: blur(20px);
    }
    /* Pannelli di stato */
    .status-panel {
        background: rgba(0, 0, 0, 0.5);
        padding: 20px;
        border-radius: var(--win11-radius);
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }
    /* Box contenuto bianco (Fix per visualizzazione) */
    .main-content {
        background: white;
        padding: 30px;
        border-radius: var(--win11-radius);
        color: #1c1c1c !important;
    }
    /* Forza colore testo scuro dentro il box bianco */
    .main-content p, .main-content h1, .main-content h2, .main-content h3, .main-content label {
        color: #1c1c1c !important;
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
if "logs" not in st.session_state:
    st.session_state.logs = []
if "remaining" not in st.session_state:
    st.session_state.remaining = 180
if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

# -----------------------------
# TIMER LOGIC
# -----------------------------
now = time.time()
delta = now - st.session_state.last_update
if delta >= 1:
    st.session_state.remaining = max(0, st.session_state.remaining - int(delta))
    st.session_state.last_update = now

remaining = st.session_state.remaining
attack_progress = int((180 - remaining)/180 * 100)

if remaining <= 0:
    st.session_state.hacked = True

# Eventi casuali
if random.random() < 0.05:
    st.session_state.logs.append(f"⚠️ {time.strftime('%H:%M:%S')} - Suspicious traffic detected")

# -----------------------------
# UI HEADER
# -----------------------------
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="status-panel"><h3 style="color:white;">⏳ TEMPO RIMASTO: {remaining}s</h3></div>', unsafe_allow_html=True)
with col2:
    score = st.session_state.resilience
    color = "#00ff00" if score > 50 else "#ff4b4b"
    st.markdown(f'<div class="status-panel"><h3 style="color:white;">🛡️ RESILIENZA: <span style="color:{color};">{score}%</span></h3></div>', unsafe_allow_html=True)

st.write("### 🔐 Encryption Progress")
st.progress(attack_progress)

# -----------------------------
# HACKED SCREEN
# -----------------------------
if st.session_state.hacked:
    st.markdown("""
        <div style="background-color:#a80000; padding:50px; border-radius:15px; text-align:center; margin-bottom:20px;">
            <h1 style="color:white !important;">🚨 SYSTEM BREACH 🚨</h1>
            <p style="color:white !important;">Ransomware encryption complete. Your files are locked.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.metric("Final Security Score", f"{score}%")
    
    if st.button("RESTART SYSTEM"):
        st.session_state.resilience = 100
        st.session_state.hacked = False
        st.session_state.remaining = 180
        st.session_state.last_update = time.time()
        st.session_state.logs = []
        st.rerun() # Forza il refresh immediato
    st.stop()

# -----------------------------
# APPLICATION AREA
# -----------------------------
app = st.selectbox(
    "Select Application:",
    ["📧 Outlook Mail", "🛡️ Defender", "⚙️ Settings", "📊 Dashboard"],
    label_visibility="collapsed"
)

# Uso di st.container() per simulare il box bianco senza rompere il layout
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    if app == "📧 Outlook Mail":
        st.subheader("📧 Outlook Web")
        st.info("Incoming: 'Urgent: Payment Declined' from security@microsoft-office.net")
        c1, c2 = st.columns(2)
        if c1.button("Verify Now"):
            st.session_state.resilience = max(0, st.session_state.resilience - 40)
            st.session_state.logs.append("❌ PHISHED! User clicked phishing link")
        if c2.button("Report Phishing"):
            st.session_state.resilience = min(100, st.session_state.resilience + 10)
            st.session_state.logs.append("✔ Phishing email reported")

    elif app == "🛡️ Defender":
        st.subheader("🛡️ Windows Defender")
        st.write("Scansione in corso...")
        if st.button("Esegui scansione completa"):
            st.session_state.logs.append("🔍 Scansione manuale avviata")
            st.success("Nessuna minaccia immediata trovata (falso positivo?)")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# SOC LOG (In basso, fuori dal box bianco)
# -----------------------------
st.write("---")
st.write("### 📜 Security Log")
for log in reversed(st.session_state.logs[-5:]):
    st.write(f"• {log}")
