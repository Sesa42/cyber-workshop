import streamlit as st

st.set_page_config(page_title="42 Hub - Microsoft 365 Simulator", layout="wide")

# --- CSS PER L'IMMERSIONE (STILE MICROSOFT) ---
st.markdown("""
    <style>
    .ms-header { background-color: #0078d4; padding: 10px; color: white; display: flex; align-items: center; }
    .ms-sidebar { background-color: #f3f2f1; border-right: 1px solid #edebe9; height: 100vh; }
    .email-item { padding: 10px; border-bottom: 1px solid #edebe9; cursor: pointer; background: white; }
    .email-item:hover { background-color: #f3f2f1; }
    .unread { border-left: 4px solid #0078d4; font-weight: bold; }
    .ms-card { background: white; padding: 20px; border: 1px solid #edebe9; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGAZIONE ---
with st.sidebar:
    st.title("42 Creative Hub")
    st.subheader("Training Environment")
    app_mode = st.selectbox("Switch Application:", ["Outlook (Email)", "OneDrive (Files)", "Admin Center (MFA)"])
    st.divider()
    st.progress(45, text="Security Readiness: 45%")

# --- 1. SIMULATORE OUTLOOK ---
if app_mode == "Outlook (Email)":
    st.markdown('<div class="ms-header">Outlook Web</div>', unsafe_allow_html=True)
    
    col_list, col_content = st.columns([1, 2])
    
    with col_list:
        st.markdown('<div class="email-item unread"><b>Microsoft Security</b><br><small>Action Required...</small></div>', unsafe_allow_html=True)
        st.markdown('<div class="email-item"><b>HR Department</b><br><small>Holiday Calendar 2026</small></div>', unsafe_allow_html=True)
        st.markdown('<div class="email-item"><b>Invoices Team</b><br><small>Invoice #88293 Pending</small></div>', unsafe_allow_html=True)

    with col_content:
        st.markdown("""
        <div class="ms-card">
            <h3>Urgent: Your Microsoft 365 subscription has expired</h3>
            <p><strong>From:</strong> microsoft-support@office-billing-secure.com</p>
            <hr>
            <p>Dear Administrator,<br>Your access to Microsoft 365 services has been suspended due to a billing error.</p>
            <p>Please update your payment method immediately to restore your files.</p>
        </div>
        """, unsafe_allow_html=True)
        
        action = st.radio("What is your move?", ["Click the 'Update Now' button", "Check the sender's email address", "Forward to IT Support"])
        if st.button("Confirm Action"):
            if "sender" in action:
                st.success("🎯 Correct! The domain 'office-billing-secure.com' is NOT an official Microsoft domain.")
            elif "Click" in action:
                st.error("🚨 CRITICAL ERROR: You just entered your credit card on a phishing site.")

# --- 2. SIMULATORE ONEDRIVE ---
elif app_mode == "OneDrive (Files)":
    st.markdown('<div class="ms-header" style="background-color: #2b579a;">OneDrive for Business</div>', unsafe_allow_html=True)
    st.write("### My Files")
    
    # Tabella file immersiva
    files = [
        {"name": "Client_Database_2026.xlsx", "sharing": "Public Link 🌐", "risk": "High"},
        {"name": "Internal_Procedures.pdf", "sharing": "Private 🔒", "risk": "Low"},
        {"name": "CEO_Personal_Notes.docx", "sharing": "Public Link 🌐", "risk": "Critical"}
    ]
    
    for f in files:
        with st.expander(f"{f['name']} - Current Sharing: {f['sharing']}"):
            st.write(f"Risk Level: {f['risk']}")
            if "Public" in f['sharing']:
                if st.button(f"Revoke Public Link for {f['name']}"):
                    st.success("Link disabled. File is now Private.")

# --- 3. ADMIN CENTER (MFA) ---
elif app_mode == "Admin Center (MFA)":
    st.markdown('<div class="ms-header" style="background-color: #000000;">Microsoft 365 Admin Center</div>', unsafe_allow_html=True)
    st.write("### Active User Sessions")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("User: Serena Saraniti\n\nDevice: iPhone 15\n\nLocation: Dublin, Ireland")
        st.button("Verify Identity", key="v1")
        
    with col_b:
        st.error("User: Serena Saraniti\n\nDevice: Unknown Linux PC\n\nLocation: Kiev, Ukraine")
        if st.button("REVOKE SESSION", key="v2"):
            st.success("Session Terminated. User prompted for MFA password reset.")
