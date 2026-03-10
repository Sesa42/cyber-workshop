import streamlit as st
import time

# Configurazione Pagina
st.set_page_config(page_title="Cyber Resilience Sandbox", layout="wide", initial_sidebar_state="collapsed")

# --- CSS: MASSIMO CONTRASTO ---
st.markdown("""
    <style>
    /* Sfondo Windows 11 */
    .stApp {
        background: url("https://4kwallpapers.com/images/wallpapers/windows-11-stock-official-blue-background-3840x2160-5630.jpg");
        background-size: cover;
        background-attachment: fixed;
    }

    /* Finestra Solida Bianca (Niente trasparenze per leggere bene) */
    .win-box {
        background-color: #ffffff !important;
        border-radius: 15px;
        padding: 40px;
        color: #000000 !important;
        box-shadow: 0 25px 50px rgba(0,0,0,0.6);
        border: 2px solid #ffffff;
        margin-bottom: 25px;
    }

    /* Forza il colore nero per ogni pezzo di testo */
    h1, h2, h3, h4, p, span, li, label, div {
        color: #000000 !important;
        font-family: 'Segoe UI', Arial, sans-serif !important;
    }

    /* Bottoni stile Windows 11 */
    .stButton>button {
        background-color: #0078d4 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
    }
    
    .stButton>button:hover {
        background-color: #005a9e !important;
    }

    /* Chat bubble Teams */
    .chat-bubble {
        background-color: #f3f2f1;
        padding: 20px;
        border-radius: 10px;
        border-left: 8px solid #6264a7;
        margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA DI SISTEMA ---
if 'score' not in st.session_state:
    st.session_state.score = 100
if 'hacked' not in st.session_state:
    st.session_state.hacked = False

# --- UI DI STATO (In alto a destra, sfondo nero per contrasto) ---
st.markdown(f"""
    <div style="background: #000000; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
        <span style="color: #ffffff !important; font-size: 1rem;">SECURITY RESILIENCE SCORE</span><br>
        <span style="color: #00ff00 !important; font-size: 2.5rem; font-weight: bold;">{st.session_state.score}%</span>
    </div>
""", unsafe_allow_html=True)

# --- SCHERMATA HACKED ---
if st.session_state.hacked:
    st.markdown("""
        <div style="background: #ff0000; padding: 50px; border-radius: 20px; text-align: center; color: white;">
            <h1 style="color: white !important;">🚨 CRITICAL SYSTEM BREACH 🚨</h1>
            <p style="color: white !important; font-size: 1.5rem;">Your actions have allowed a cyber-attack to succeed.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("RESTART SIMULATION"):
        st.session_state.score = 100
        st.session_state.hacked = False
        st.rerun()
    st.stop()

# --- NAVIGAZIONE ---
tab = st.selectbox("CHOOSE APPLICATION", 
                  ["📧 OUTLOOK", "📂 ONEDRIVE", "💬 TEAMS CHAT", "🛡️ DEFENDER"], 
                  label_visibility="collapsed")

# --- SCENARIO: EMAIL ---
if tab == "📧 OUTLOOK":
    st.markdown('<div class="win-box">', unsafe_allow_html=True)
    st.write("### 📩 Inbox: (1) Urgent Message")
    st.write("**From:** IT Service <security@m-office365-admin.net>")
    st.write("**Subject:** Immediate Action: Account Lockout Predicted")
    st.write("Someone from Russia attempted to login. Click below to verify your identity.")
    
    c1, c2 = st.columns(2)
    if c1.button("CLICK TO VERIFY"):
        st.session_state.score -= 40
        st.error("❌ FAILED: The domain '.net' is a phishing trap. Your password has been stolen.")
    if c2.button("REPORT AS PHISHING"):
        st.session_state.score += 15
        st.success("✅ EXCELLENT: You spotted the fake domain. +15 pts")
    st.markdown('</div>', unsafe_allow_html=True)

# --- SCENARIO: DRIVE ---
elif tab == "📂 ONEDRIVE":
    st.markdown('<div class="win-box">', unsafe_allow_html=True)
    st.write("### 📂 OneDrive: Sharing Audit")
    st.write("Audit your sensitive folders. Fix any 'Public' sharing settings.")
    
    files = [["Financial_Report_2026.xlsx", "Public Link"], ["HR_Contracts.zip", "Anyone with link"]]
    for f in files:
        col_a, col_b = st.columns([3, 1])
        col_a.write(f"⚠️ **{f[0]}** | Status: {f[1]}")
        if col_b.button("Make Private", key=f[0]):
            st.success("Access Restricted!")
            st.session_state.score += 10
    st.markdown('</div>', unsafe_allow_html=True)

# --- SCENARIO: TEAMS ---
elif tab == "💬 TEAMS CHAT":
    st.markdown('<div class="win-box">', unsafe_allow_html=True)
    st.write("### 💬 Microsoft Teams Chat")
    st.markdown("""<div class="chat-bubble"><b>External User (IT Helpdesk):</b><br>
    Hi Serena, we are fixing your email sync. I've sent an <b>MFA code</b> to your phone. 
    Please paste it here so I can authorize the update.</div>""", unsafe_allow_html=True)
    
    c_yes, c_no = st.columns(2)
    if c_yes.button("PASTE CODE"):
        st.session_state.hacked = True
        st.rerun()
    if c_no.button("REPORT USER"):
        st.success("🏆 PROTECTED! IT will NEVER ask for MFA codes via chat. +25 pts")
        st.session_state.score += 25
    st.markdown('</div>', unsafe_allow_html=True)

# --- SCENARIO: DEFENDER ---
elif tab == "🛡️ DEFENDER":
    st.markdown('<div class="win-box">', unsafe_allow_html=True)
    st.write("### 🛡️ Microsoft Defender Security")
    st.warning("Found a USB Flash Drive connected: 'NEW_DRIVE_D'")
    st.write("You found this drive in the breakroom. What do you do?")
    
    if st.button("SCAN AND OPEN"):
        st.error("🚨 MALWARE! The drive contained a hidden script that stole your local data.")
        st.session_state.score -= 50
    if st.button("HAND TO SECURITY"):
        st.success("✅ SMART: Never plug in unknown devices. +20 pts")
        st.session_state.score += 20
    st.markdown('</div>', unsafe_allow_html=True)
