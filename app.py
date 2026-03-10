import streamlit as st

st.set_page_config(page_title="Windows 11 Cyber Simulator", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS: WINDOWS 11 LOOK & FEEL ---
st.markdown("""
    <style>
    .main { background: linear_gradient(to bottom, #0078d4, #001e36); background-attachment: fixed; }
    .stApp { background: url("https://4kwallpapers.com/images/wallpapers/windows-11-stock-official-blue-background-3840x2160-5630.jpg"); background-size: cover; }
    
    /* Window Style */
    .win-window {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(15px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 20px;
        color: #1a1a1a;
        min-height: 500px;
    }
    
    /* Taskbar Style */
    .taskbar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 50px;
        background: rgba(243, 243, 243, 0.8);
        backdrop-filter: blur(10px);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }
    
    .task-icon { margin: 0 15px; cursor: pointer; width: 32px; transition: 0.2s; }
    .task-icon:hover { transform: scale(1.2); }
    </style>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT (SCORE & PROGRESS) ---
if 'score' not in st.session_state:
    st.session_state.score = 100
if 'completed' not in st.session_state:
    st.session_state.completed = []

# --- HEADER: SCORE & STATUS ---
col_s1, col_s2 = st.columns([4, 1])
with col_s2:
    st.metric("Resilience Score", f"{st.session_state.score}/100")

# --- NAVIGATION MENU (TASKBAR SIMULATION) ---
menu = st.selectbox("Switch App:", ["🏠 Desktop / Start", "📧 Outlook", "📂 File Explorer", "🔐 Security Center"], label_visibility="collapsed")

# --- 1. DESKTOP / START ---
if menu == "🏠 Desktop / Start":
    st.markdown('<div class="win-window"><h1>Welcome to Windows 11</h1><p>Select an app from the dropdown to start your Cyber Readiness audit.</p></div>', unsafe_allow_html=True)

# --- 2. OUTLOOK (PHISHING SCENARIOS) ---
elif menu == "📧 Outlook":
    st.markdown('<div class="win-window"><h2>Outlook Web</h2>', unsafe_allow_html=True)
    scenario = st.radio("Select Email to Review:", ["Email 1: IT Support", "Email 2: Unpaid Invoice", "Email 3: CEO Message"])
    
    if scenario == "Email 1: IT Support":
        st.info("**From:** admin@m-office365-security.com\n\n**Subject:** MFA Verification Required")
        st.write("Click here to re-enable your account.")
        choice = st.button("Click Link & Login")
        if choice:
            st.session_state.score -= 20
            st.error("❌ WRONG: The domain 'm-office365-security.com' is fake. -20 Points.")
            
    elif scenario == "Email 2: Unpaid Invoice":
        st.info("**From:** accounts@real-vendor.com\n\n**Subject:** Invoice_9921.zip")
        st.write("Please find the attached invoice for last month.")
        choice = st.button("Download & Open ZIP")
        if choice:
            st.session_state.score -= 30
            st.error("🚨 MALWARE: ZIP files from unexpected emails often contain ransomware. -30 Points.")

    elif scenario == "Email 3: CEO Message":
        st.info("**From:** serena.ceo.42@gmail.com\n\n**Subject:** Quick favor")
        st.write("I'm in a meeting. Can you buy 5 Amazon gift cards for a client?")
        choice = st.button("Reply & Ask for details")
        if choice:
            st.session_state.score -= 25
            st.error("⚠️ BEC ATTACK: Business Email Compromise. Your CEO would never use Gmail for this. -25 Points.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. FILE EXPLORER (DATA GOVERNANCE) ---
elif menu == "📂 File Explorer":
    st.markdown('<div class="win-window"><h2>OneDrive - 42 Creative Hub</h2>', unsafe_allow_html=True)
    
    files = [
        {"name": "Client_List_Confidential.csv", "perm": "Public Link", "action": "Restrict Access"},
        {"name": "Meeting_Notes.docx", "perm": "Private", "action": "Share Publicly"},
        {"name": "Company_Bank_Details.xlsx", "perm": "Anyone with link", "action": "Restrict Access"}
    ]
    
    for i, f in enumerate(files):
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.write(f"📄 {f['name']}")
        c2.write(f"Status: {f['perm']}")
        if c3.button("Execute Action", key=f"btn_{i}"):
            if "Restrict" in f['action']:
                st.success("✅ Secure! Access restricted. +10 Points.")
                st.session_state.score += 10
            else:
                st.error("❌ Vulnerability Created! You just made a file public. -15 Points.")
                st.session_state.score -= 15
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. SECURITY CENTER (INCIDENT RESPONSE) ---
elif menu == "🔐 Security Center":
    st.markdown('<div class="win-window"><h2>Windows Security - Active Alerts</h2>', unsafe_allow_html=True)
    st.warning("Critical Alert: Unusual login from St. Petersburg, Russia")
    
    response = st.selectbox("Immediate Action:", ["Ignore", "Call Employee", "Disable Account & Force Password Reset", "Wait for IT"])
    if st.button("Confirm Response"):
        if "Disable" in response:
            st.success("🏆 CORRECT! Containment is the first priority. Security Score Improved.")
            st.session_state.score += 20
        else:
            st.error("❌ TOO SLOW: The attacker has now encrypted your files. -40 Points.")
            st.session_state.score -= 40
    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<br><br><p style='text-align: center; color: white;'>42 Creative Hub Cyber Resilience Sandbox v2.0</p>", unsafe_allow_html=True)
