import streamlit as st

# Page configuration
st.set_page_config(page_title="42 Creative Hub - Cyber Sandbox", layout="wide", page_icon="🛡️")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #0078d4; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Main Title
st.title("🛡️ 42 Creative Hub: Cybersecurity Resilience Sandbox")
st.markdown("---")

# Sidebar Navigation
with st.sidebar:
    st.image("https://via.placeholder.com/150", caption="42 Creative Hub") # Replace with your logo URL later
    st.header("Workshop Modules")
    choice = st.radio("Select Environment:", 
                      ["🏠 Dashboard", 
                       "📧 Email Simulator", 
                       "📁 Data Governance", 
                       "🔑 Identity & MFA"])
    st.divider()
    st.write("Facilitator: **Serena Saraniti**")

# --- MODULE LOGIC ---

if choice == "🏠 Dashboard":
    st.subheader("Welcome to the Cyber Resilience Workshop!")
    st.write("This is a safe environment to practice your cybersecurity skills without affecting production systems.")
    st.info("Objective: Move from theory to practice and improve your company's security score.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Simulated Threats", "12", "Active")
    col2.metric("Public Links Found", "3", "-20%")
    col3.metric("Security Score", "45%", "+5% today")

elif choice == "📧 Email Simulator":
    st.subheader("Exercise: Phishing Recognition")
    st.write("Analyze the following email. Is there anything suspicious?")
    
    with st.container():
        st.markdown("""
        <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; background-color: white; color: #333;">
            <strong>From:</strong> Microsoft Support <span style="color: #888;">&lt;security-alert@m1crosoft-cloud.com&gt;</span><br>
            <strong>Subject:</strong> Action Required: Your account has been suspended!
            <hr>
            Dear User, we detected unusual activity on your account. To prevent permanent suspension, please verify your identity immediately by clicking the button below:
        </div>
        """, unsafe_allow_html=True)
        st.write("") # Spacer
        
        col_btn1, col_btn2 = st.columns(2)
        if col_btn1.button("🔗 ACCESS PORTAL"):
            st.error("🚨 PHISHED! You clicked a malicious link. Notice the sender domain: 'm1crosoft' (with a number '1' instead of 'i').")
        if col_btn2.button("🚩 REPORT AS PHISHING"):
            st.success("✅ WELL DONE! You correctly identified a typosquatting domain and a sense of false urgency.")

elif choice == "📁 Data Governance":
    st.subheader("Exercise: Permission Audit")
    st.write("These files are in your corporate shared drive. Which ones are over-exposed?")
    
    col_h1, col_h2, col_h3 = st.columns([2, 2, 1])
    col_h1.write("**Filename**")
    col_h2.write("**Current Access**")
    col_h3.write("**Action**")
    
    # File 1
    c1, c2, c3 = st.columns([2, 2, 1])
    c1.text("Payroll_2024_Q1.pdf")
    c2.warning("Public (Anyone with the link)")
    if c3.button("Make Private", key="f1"):
        st.success("Access restricted to HR Team only!")

    # File 2
    c4, c5, c6 = st.columns([2, 2, 1])
    c4.text("Project_Alpha_Notes.docx")
    c5.success("Internal Only")
    c6.write("-")

elif choice == "🔑 Identity & MFA":
    st.subheader("Exercise: Multi-Factor Authentication")
    st.warning("A login attempt was detected from an unrecognized device.")
    
    st.info("""
    **Login Details:**
    - Device: Chrome Browser on Linux
    - Location: Kiev, Ukraine
    - Time: Just now
    """)
    
    col_y, col_n = st.columns(2)
    if col_y.button("✅ IT'S ME (Approve)"):
        st.error("❌ FATAL ERROR! You just granted access to a remote attacker.")
    if col_n.button("❌ IT'S NOT ME (Deny)"):
        st.success("✅ PROTECTED! You blocked the unauthorized access and secured the account.")
