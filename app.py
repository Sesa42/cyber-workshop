import streamlit as st

st.set_page_config(page_title="Windows 11 Cyber Simulator", layout="wide", initial_sidebar_state="collapsed")

# --- CSS: FIXED READABILITY & WIN11 STYLE ---
st.markdown("""
    <style>
    .stApp {
        background: url("https://4kwallpapers.com/images/wallpapers/windows-11-stock-official-blue-background-3840x2160-5630.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Solid Glass Style for Readability */
    .win-card {
        background: rgba(255, 255, 255, 0.95); /* Più opaco per leggere bene */
        border-radius: 12px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        padding: 25px;
        color: #1e1e1e;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }

    .taskbar-sim {
        background: rgba(243, 243, 243, 0.9);
        padding: 10px;
        border-radius: 50px;
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
        border: 1px solid rgba(255,255,255,0.5);
    }
    
    h1, h2, h3, p { color: #1e1e1e !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'score' not in st.session_state:
    st.session_state.score = 100
if 'actions_taken' not in st.session_state:
    st.session_state.actions_taken = 0

# --- TOP BAR: SCORE ---
c1, c2 = st.columns([5, 1])
with c2:
    st.markdown(f"""
        <div style="background: rgba(0,0,0,0.7); padding: 10px; border-radius: 10px; text-align: center;">
            <span style="color: white; font-size: 0.8rem;">Resilience Score</span><br>
            <span style="color: #00ff00; font-size: 1.5rem; font-weight: bold;">{st.session_state.score}</span>
        </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
app_select = st.selectbox("Search or Select App:", 
                         ["🏠 Desktop", "📧 Outlook", "📂 File Explorer", "🛡️ Microsoft Defender"], 
                         label_visibility="collapsed")

# --- 1. DESKTOP ---
if app_select == "🏠 Desktop":
    st.markdown("""
        <div class="win-card">
            <h1>Good morning, Serena</h1>
            <p>Your system is currently under audit. Please check your applications for potential security risks.</p>
            <hr>
            <h4>System Tasks:</h4>
            <ul>
                <li>Review 3 unread critical emails in Outlook.</li>
                <li>Audit sharing permissions in OneDrive.</li>
                <li>Verify 1 active threat in Defender.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# --- 2. OUTLOOK (SCENARI COMPLESSI) ---
elif app_select == "📧 Outlook":
    st.markdown('<div class="win-card"><h2>Outlook Web - Inbox</h2>', unsafe_allow_html=True)
    
    scenario = st.selectbox("View Email:", [
        "Select an email...",
        "1. Internal: Bonus Payment Link",
        "2. System: Unusual Login Attempt",
        "3. Client: New Project Proposal"
    ])

    if scenario == "1. Internal: Bonus Payment Link":
        st.write("**From:** HR-Department <noreply@company-hr-portal.net>")
        st.write("**Subject:** Urgent: Click to claim your 2026 performance bonus")
        st.image("https://img.icons8.com/color/48/000000/info.png", width=30)
        st.info("Wait! Check the link before clicking: `https://bit.ly/claim-bonus-2026` (Points to an external shortener)")
        
        col_a, col_b, col_c = st.columns(3)
        if col_a.button("Click & Claim"):
            st.session_state.score -= 40
            st.error("🚨 FAIL: HR never uses link shorteners for payroll. You've been phished. -40 pts")
        if col_b.button("Reply & Ask Info"):
            st.session_state.score -= 10
            st.warning("⚠️ RISKY: Replying confirms your email is active. Better to call HR directly. -10 pts")
        if col_c.button("Report to IT"):
            st.session_state.score += 20
            st.success("🎯 EXCELLENT: You spotted the suspicious domain and short-link. +20 pts")

    elif scenario == "2. System: Unusual Login Attempt":
        st.write("**From:** Microsoft Security <account-security-noreply@microsoft.com>")
        st.write("**Subject:** Security alert for your account")
        st.write("Someone just signed in to your account from: **Nairobi, Kenya**")
        
        choice = st.radio("Is this you?", ["Yes, it was me", "No, block account", "I am not sure, check my login history"])
        if st.button("Confirm Response"):
            if "block" in choice:
                st.success("✅ PROACTIVE: Account secured immediately. +15 pts")
                st.session_state.score += 15
            elif "history" in choice:
                st.info("ℹ️ GOOD: Verification is key. No points lost.")
            else:
                st.error("❌ DANGEROUS: You allowed an attacker into the system. -50 pts")
                st.session_state.score -= 50

# --- 3. FILE EXPLORER ---
elif app_select == "📂 File Explorer":
    st.markdown('<div class="win-card"><h2>OneDrive - Permissions Audit</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 1])
    col1.write("**File Name**")
    col2.write("**Shared With**")
    col3.write("**Action**")

    # Scenario: Over-sharing
    files = [
        ["Financial_Report.xlsx", "Anyone with the link (Edit)", "Restrict"],
        ["Team_Photo.jpg", "Anyone with the link (View)", "Keep"],
        ["CEO_Private_Keys.txt", "Public", "DELETE IMMEDIATELY"]
    ]

    for f in files:
        c1, c2, c3 = st.columns([2, 2, 1])
        c1.text(f[0])
        c2.text(f[1])
        if c3.button("Fix", key=f[0]):
            if f[2] == "Restrict" or f[2] == "DELETE IMMEDIATELY":
                st.success("✅ Secured!")
                st.session_state.score += 10
            else:
                st.warning("Low risk, but good for privacy.")

# --- 4. MICROSOFT DEFENDER ---
elif app_select == "🛡️ Microsoft Defender":
    st.markdown('<div class="win-card"><h2>Windows Security Center</h2>', unsafe_allow_html=True)
    st.error("Found 1 threat: **Trojan:Win32/CredentialStealer.A**")
    st.write("Source: `Downloads/invoice.exe`")
    
    act = st.selectbox("Action:", ["Quarantine", "Allow on device", "Ignore"])
    if st.button("Apply Action"):
        if act == "Quarantine":
            st.success("🏆 Safe! Threat removed. +20 pts")
            st.session_state.score += 20
        else:
            st.session_state.score = 0
            st.error("💥 SYSTEM COMPROMISED: Your credentials have been stolen. Score reset to 0.")

st.markdown('</div>', unsafe_allow_html=True)
