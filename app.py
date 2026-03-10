import streamlit as st
import time

# Configurazione Pagina
st.set_page_config(page_title="Cyber Resilience Sandbox", layout="wide", initial_sidebar_state="collapsed")

# --- CSS: MASSIMO CONTRASTO E LEGGIBILITÀ ---
st.markdown("""
    <style>
    /* Sfondo Windows 11 */
    .stApp {
        background: url("https://4kwallpapers.com/images/wallpapers/windows-11-stock-official-blue-background-3840x2160-5630.jpg");
        background-size: cover;
        background-attachment: fixed;
    }

    /* Finestra BIANCA SOLIDA (Niente trasparenze) */
    .win-content {
        background-color: #ffffff !important;
        border-radius: 12px;
        padding: 40px;
        color: #000000 !important;
        box-shadow: 0 20px 60px rgba(0,0,0,0.7);
        border: 1px solid #d1d1d1;
        margin-top: 20px;
    }

    /* Forza il testo NERO ovunque */
    h1, h2, h3, h4, p, span, li, label, div, .stMarkdown {
        color: #000000 !important;
        font-family: 'Segoe UI', Arial, sans-serif !important;
    }

    /* Bottoni Blu Microsoft */
    .stButton>button {
        background-color: #0078d4 !important;
        color: white !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        border: none !important;
        height: 3em !important;
        width: 100% !important;
    }
    
    /* Timer e Score Header */
    .status-bar {
        background: #000000;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white !important;
        margin-bottom: 10px;
    }

    /* Box Messaggi Teams */
    .teams-msg {
        background-color: #f3f2f1;
        border-left: 6px solid #6264a7;
        padding: 20px;
        margin: 15px 0;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA DI SISTEMA ---
if 'resilience' not in st.session_state:
    st.session_state.resilience = 100
if 'hacked' not in st.session_state:
    st.session_state.hacked = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

# --- TIMER (180s) ---
elapsed = time.time() - st.session_state.start_time
remaining = max(0, int(180 - elapsed))
if remaining == 0: st.session_state.hacked = True

# --- HEADER STATUS ---
col_t, col_s = st.columns([1, 1])
with col_t:
    st.markdown(f'<div class="status-bar"><span style="color:white !important;">⏳ TIME REMAINING: {remaining}s</span></div>', unsafe_allow_html=True)
with col_s:
    st.markdown(f'<div class="status-bar"><span style="color:white !important;">🛡️ RESILIENCE SCORE: {st.session_state.resilience}%</span></div>', unsafe_allow_html=True)

# --- SCHERMATA RANSOMWARE ---
if st.session_state.hacked:
    st.markdown("""
        <div style="background: #7d0000; padding: 60px; border-radius: 15px; text-align: center; color: white;">
            <h1 style="color: white !important;">🚨 SYSTEM COMPROMISED 🚨</h1>
            <p style="color: white !important;">Emergency protocols failed. Cyber-attack successful.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("REBOOT SYSTEM"):
        st.session_state.resilience = 100
        st.session_state.hacked = False
        st.session_state.start_time = time.time()
        st.rerun()
    st.stop()

# --- APP NAV ---
app = st.selectbox("CHOOSE SYSTEM APP", 
                  ["📧 OUTLOOK", "📂 ONEDRIVE", "💬 TEAMS CHAT", "🛡️ DEFENDER", "🛠️ SYSTEM SETTINGS"], 
                  label_visibility="collapsed")

st.markdown('<div class="win-content">', unsafe_allow_html=True)

# --- SCENARI ---
if app == "📧 OUTLOOK":
    st.write("### 📬 Outlook: New Security Alert")
    st.write("**From:** Microsoft Admin <no-reply@m-office365-verify.net>")
    st.write("**Subject:** Urgent: Unusual activity detected in your account")
    st.write("We detected a login from Lagos, Nigeria. Click to verify your identity.")
    
    c1, c2, c3 = st.columns(3)
    if c1.button("Check Technical Headers"):
        st.info("Technical Info: Domain '.net' is not official. Return-path: unknown-server.ru")
    if c2.button("Click & Verify"):
        st.session_state.resilience -= 40
        st.error("❌ PHISHED! You gave your credentials to a fake site.")
    if c3.button("Report to IT"):
        st.session_state.resilience += 20
        st.success("🎯 Correct! Resilience increased.")

elif app == "💬 TEAMS CHAT":
    st.write("### 💬 Microsoft Teams Chat")
    st.markdown("""<div class="teams-msg"><b>External (IT Support - Mark):</b><br>
    Hi Serena, I'm verifying your account sync. I've sent a code to your phone. 
    Can you please tell me the 6-digit code?</div>""", unsafe_allow_html=True)
    
    col_y, col_n = st.columns(2)
    if col_y.button("Give Code"):
        st.session_state.hacked = True
        st.rerun()
    if col_n.button("Decline & Block"):
        st.success("🏆 Safe! IT will never ask for MFA codes via chat.")
        st.session_state.resilience += 25

elif app == "📂 ONEDRIVE":
    st.write("### 📂 OneDrive: Sharing Review")
    st.write("Audit the access for the following folders:")
    
    files = [["Accounting_Private.zip", "Anyone with link"], ["CEO_Notes.docx", "Public"]]
    for f in files:
        c1, c2 = st.columns([3, 1])
        c1.write(f"⚠️ **{f[0]}** | Status: {f[1]}")
        if c2.button("Restrict Access", key=f[0]):
            st.success("Fixed!")
            st.session_state.resilience += 10

elif app == "🛡️ DEFENDER":
    st.write("### 🛡️ Microsoft Defender Security")
    st.warning("Hardware Alert: Unknown USB drive plugged in (PARKING_LOT_FIND)")
    if st.button("Open Folder to find owner"):
        st.error("🚨 MALWARE! The drive contained a keylogger. Data is being stolen.")
        st.session_state.resilience -= 50
    if st.button("Disconnect & Report"):
        st.success("Perfect! Unknown USBs are never safe.")
        st.session_state.resilience += 20

elif app == "🛠️ SYSTEM SETTINGS":
    st.write("### 🛠️ System Settings: Shadow IT")
    st.write("Identify and remove unauthorized applications:")
    apps = [["Office 365", "Official"], ["Free-VPN-Ultimate", "Unauthorized"], ["CryptoMiner.exe", "Malicious"]]
    for a in apps:
        c_a, c_b = st.columns([3, 1])
        c_a.write(f"**{a[0]}** | Type: {a[1]}")
        if a[1] != "Official" and c_b.button("Uninstall", key=a[0]):
            st.success("Removed!")
            st.session_state.resilience += 15

st.markdown('</div>', unsafe_allow_html=True)
