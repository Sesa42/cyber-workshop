import streamlit as st
import time

# Configurazione Pagina
st.set_page_config(page_title="Cyber Resilience Sandbox", layout="wide", initial_sidebar_state="collapsed")

# --- CSS: ULTIMA GENERAZIONE PER CONTRASTO TOTALE ---
st.markdown("""
    <style>
    /* Sfondo Windows 11 */
    .stApp {
        background: url("https://4kwallpapers.com/images/wallpapers/windows-11-stock-official-blue-background-3840x2160-5630.jpg");
        background-size: cover;
        background-attachment: fixed;
    }

    /* CONTAINER BIANCO SOLIDO - Rimuove ogni trasparenza */
    .content-container {
        background-color: white !important;
        padding: 40px;
        border-radius: 15px;
        border: 2px solid #d1d1d1;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-top: 20px;
    }

    /* FORZA TESTO NERO - Indispensabile per la leggibilità */
    h1, h2, h3, h4, p, li, span, label, div, .stMarkdown {
        color: #1a1a1a !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        opacity: 1 !important;
    }

    /* BOTTONI BLU MICROSOFT - Visibili e chiari */
    .stButton>button {
        background-color: #0078d4 !important;
        color: white !important;
        border-radius: 4px !important;
        border: none !important;
        height: 3.5em !important;
        font-weight: bold !important;
        width: 100%;
    }

    /* BARRA DI STATO NERA - Per far risaltare Score e Timer */
    .status-panel {
        background-color: #000000 !important;
        color: #ffffff !important;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #444;
    }

    /* CHAT TEAMS - Stile bolla */
    .teams-bubble {
        background-color: #f3f2f1;
        border-left: 6px solid #6264a7;
        padding: 20px;
        margin: 15px 0;
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

# --- TIMER (180 secondi) ---
elapsed = time.time() - st.session_state.start_time
remaining = max(0, int(180 - elapsed))
if remaining == 0: st.session_state.hacked = True

# --- UI DI STATO ---
col_timer, col_score = st.columns(2)
with col_timer:
    st.markdown(f'<div class="status-panel"><h3 style="color:white !important;">⏳ TIME: {remaining}s</h3></div>', unsafe_allow_html=True)
with col_score:
    st.markdown(f'<div class="status-panel"><h3 style="color:white !important;">🛡️ RESILIENCE: {st.session_state.resilience}%</h3></div>', unsafe_allow_html=True)

# --- SCHERMATA RANSOMWARE (ROSSA) ---
if st.session_state.hacked:
    st.markdown("""
        <div style="background-color: #a80000; padding: 100px; border-radius: 15px; text-align: center;">
            <h1 style="color: white !important;">🚨 SYSTEM BREACH DETECTED 🚨</h1>
            <p style="color: white !important; font-size: 1.5rem;">The organization is now under a Ransomware attack.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("SYSTEM RESTORE"):
        st.session_state.resilience = 100
        st.session_state.hacked = False
        st.session_state.start_time = time.time()
        st.rerun()
    st.stop()

# --- APP SELECTOR ---
app = st.selectbox("Search or Select Application:", 
                  ["📧 Outlook Mail", "📂 OneDrive Audit", "💬 Teams (Internal Chat)", "🛡️ Microsoft Defender", "⚙️ System Settings"],
                  label_visibility="collapsed")

# --- CONTENITORE PRINCIPALE ---
st.markdown('<div class="content-container">', unsafe_allow_html=True)

if app == "📧 Outlook Mail":
    st.write("## 📧 Outlook Web - Security Alert")
    st.write("**From:** IT Admin (security-noreply@microsoft-office.net)")
    st.write("**Subject:** Immediate Action: Account Compromise Detected")
    st.info("Technical Analysis: Sender domain uses '.net' instead of '.com'. Link points to a URL shortener.")
    
    col1, col2 = st.columns(2)
    if col1.button("Verify Identity Now"):
        st.session_state.resilience -= 40
        st.error("❌ PHISHED! You entered credentials on a fake site. Domain '.net' was a trap.")
    if col2.button("Report as Phishing"):
        st.session_state.resilience += 20
        st.success("🎯 Correct! You identified the spoofed domain.")

elif app == "💬 Teams (Internal Chat)":
    st.write("## 💬 Microsoft Teams - New Chat")
    st.markdown("""<div class="teams-bubble"><b>External (IT Support - Mark):</b><br>
    Hi Serena, I'm verifying your account migration. I've sent a 6-digit MFA code to your phone. 
    Can you please share it here to complete the process?</div>""", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    if col_a.button("Share MFA Code"):
        st.session_state.hacked = True
        st.rerun()
    if col_b.button("Refuse & Report User"):
        st.success("🏆 PROTECTED! IT will NEVER ask for MFA codes via chat. This was Social Engineering.")
        st.session_state.resilience += 30

elif app == "📂 OneDrive Audit":
    st.write("## 📂 OneDrive - Sharing Review")
    st.write("The following critical folders are currently shared with **'Anyone with the link'**:")
    
    folders = [["Financial_Report_2025.zip", "Public"], ["Employee_IDs.pdf", "Public"]]
    for f in folders:
        c1, c2 = st.columns([3, 1])
        c1.write(f"⚠️ **{f[0]}** | Risk: High Exposure")
        if c2.button(f"Make Private", key=f[0]):
            st.success("Permission revoked!")
            st.session_state.resilience += 10

elif app == "🛡️ Microsoft Defender":
    st.write("## 🛡️ Windows Security Center")
    st.warning("New Hardware: Unknown USB drive detected (Label: 'BACKUP_DRIVE')")
    st.write("Background: You found this drive in the coffee area. What is your action?")
    
    if st.button("Open Folder to Identify Owner"):
        st.error("🚨 MALWARE! The drive contained a 'Rubber Ducky' script. Keystrokes are being recorded.")
        st.session_state.resilience -= 50
    if st.button("Deliver to IT Security"):
        st.success("✅ SMART: Plugging in unknown USBs is a critical security violation.")
        st.session_state.resilience += 20

elif app == "⚙️ System Settings":
    st.write("## ⚙️ Settings - Installed Apps")
    st.write("Shadow IT Detection: Identify and remove unauthorized software.")
    
    soft = [["Microsoft Office", "Safe"], ["Free-VPN-Pro (Unsigned)", "Risk"], ["Advanced_Web_Crawler.exe", "Risk"]]
    for s in soft:
        ca, cb = st.columns([3, 1])
        ca.write(f"**{s[0]}** | Status: {s[1]}")
        if s[1] == "Risk" and cb.button("Uninstall", key=s[0]):
            st.success("App Removed!")
            st.session_state.resilience += 15

st.markdown('</div>', unsafe_allow_html=True)
