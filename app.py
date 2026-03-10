import streamlit as st
import time

st.set_page_config(page_title="Win11 Cyber Emergency", layout="wide", initial_sidebar_state="collapsed")

# --- EMERGENCY ENGINE (CSS) ---
st.markdown("""
    <style>
    .stApp { background: url("https://4kwallpapers.com/images/wallpapers/windows-11-stock-official-blue-background-3840x2160-5630.jpg"); background-size: cover; }
    .win-window { background: rgba(255, 255, 255, 0.98); border-radius: 12px; padding: 30px; color: #1a1a1a !important; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
    .ransom-bg { background-color: #7d0000 !important; color: white !important; padding: 50px; border-radius: 12px; text-align: center; }
    h1, h2, h3, p, span { color: #1a1a1a !important; }
    .timer-text { font-size: 2rem; font-weight: bold; color: #d11a2a !important; }
    .chat-bubble { background: #e1dfdd; padding: 10px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #0078d4; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'resilience' not in st.session_state:
    st.session_state.resilience = 100
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'hacked' not in st.session_state:
    st.session_state.hacked = False

# --- TIMER LOGIC (180 Seconds per dare spazio ai nuovi scenari) ---
limit = 180 
elapsed = time.time() - st.session_state.start_time
remaining = max(0, int(limit - elapsed))

if remaining == 0:
    st.session_state.hacked = True

# --- TOP INTERFACE ---
c1, c2, c3 = st.columns([3, 1, 1])
with c2:
    st.markdown(f'<p class="timer-text">⏳ {remaining}s</p>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div style="background:#1e1e1e; padding:10px; border-radius:5px; color:white !important; text-align:center;">RESILIENCE: {st.session_state.resilience}%</div>', unsafe_allow_html=True)

# --- RANSOMWARE SCREEN ---
if st.session_state.hacked:
    st.markdown("""<div class="ransom-bg"><h1 style="color:white !important;">🚨 SYSTEM COMPROMISED 🚨</h1><p style="color:white !important;">Critical failure. Cybersecurity protocols breached.</p></div>""", unsafe_allow_html=True)
    if st.button("REBOOT & RETRY"):
        st.session_state.resilience = 100
        st.session_state.start_time = time.time()
        st.session_state.hacked = False
        st.rerun()
    st.stop()

# --- APP SELECTION ---
app = st.selectbox("Select Application", 
                  ["📧 Outlook", "📂 OneDrive", "💬 Teams (Social Engineering)", "🛠️ Settings (Shadow IT)", "🛡️ Defender"], 
                  label_visibility="collapsed")

# --- SCENARIO 1: OUTLOOK ---
if app == "📧 Outlook":
    st.markdown('<div class="win-window"><h2>Outlook - Inbox</h2>', unsafe_allow_html=True)
    st.write("**Subject: Action Required: Your payment was declined**")
    st.write("Sender: `accounts-pay-support@outlook-verify.net`")
    col1, col2 = st.columns(2)
    if col1.button("Check Domain Info"):
        st.info("Technical Insight: The sender uses '.net' instead of '.com'. IP address is blacklisted.")
    if col2.button("Report Phishing"):
        st.success("Correct! +15% Resilience")
        st.session_state.resilience += 15
    st.markdown('</div>', unsafe_allow_html=True)

# --- SCENARIO 2: ONEDRIVE ---
elif app == "📂 OneDrive":
    st.markdown('<div class="win-window"><h2>OneDrive - File Audit</h2>', unsafe_allow_html=True)
    st.write("Review files with 'Anyone with the link' access:")
    files = [["Accounting_2025.xlsx", "🔴"], ["Company_Logo.png", "🟢"], ["Customer_List.csv", "🔴"]]
    for f in files:
        col_f, col_btn = st.columns([3, 1])
        col_f.write(f"{f[1]} {f[0]}")
        if col_btn.button(f"Revoke", key=f[0]):
            st.success(f"Access restricted for {f[0]}")
            st.session_state.resilience += 5
    st.markdown('</div>', unsafe_allow_html=True)

# --- SCENARIO 3: SOCIAL ENGINEERING (TEAMS) ---
elif app == "💬 Teams (Social Engineering)":
    st.markdown('<div class="win-window"><h2>Microsoft Teams</h2>', unsafe_allow_html=True)
    st.markdown("""<div class="chat-bubble"><b>External User (Marco - IT Consultant):</b><br>Hi Serena, I'm working on the server migration. I need the MFA bypass code sent to your phone to finish the update. Can you send it?</div>""", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    if col_a.button("Send Code"):
        st.error("🚨 SCAM! Never share MFA codes. An attacker just logged into your admin account.")
        st.session_state.resilience -= 50
    if col_b.button("Block & Call IT"):
        st.success("Perfect! You recognized a Social Engineering attempt. +20% Resilience")
        st.session_state.resilience += 20
    st.markdown('</div>', unsafe_allow_html=True)

# --- SCENARIO 4: SHADOW IT (SETTINGS) ---
elif app == "🛠️ Settings (Shadow IT)":
    st.markdown('<div class="win-window"><h2>System Settings - Installed Apps</h2>', unsafe_allow_html=True)
    st.write("Audit unauthorized software installed by employees:")
    apps = [["Official Office 365", "Safe"], ["Free-PDF-Converter-Pro (Unsigned)", "Suspicious"], ["BitTorrent", "Risk"]]
    for a in apps:
        col_a, col_st, col_btn = st.columns([2, 1, 1])
        col_a.write(a[0])
        col_st.write(a[1])
        if a[1] != "Safe" and col_btn.button("Uninstall", key=a[0]):
            st.success(f"{a[0]} removed.")
            st.session_state.resilience += 10
    st.markdown('</div>', unsafe_allow_html=True)

# --- SCENARIO 5: DEFENDER (PHYSICAL THREAT) ---
elif app == "🛡️ Defender":
    st.markdown('<div class="win-window"><h2>Windows Defender - Hardware Alert</h2>', unsafe_allow_html=True)
    st.warning("New USB Device Connected: 'SANDISK_128GB'")
    st.write("Background: You found this USB in the parking lot and plugged it in to find the owner.")
    
    if st.button("Run Scan"):
        st.error("🚨 VIRUS DETECTED! The USB contained a 'Rubber Ducky' script that is stealing your keystrokes.")
        st.session_state.resilience -= 40
    st.markdown('</div>', unsafe_allow_html=True)
