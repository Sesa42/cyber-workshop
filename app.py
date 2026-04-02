import streamlit as st
import time
import random
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# 1. PAGE CONFIGURATION (Only once!)
# -----------------------------
st.set_page_config(
    page_title="Cyber Resilience Sandbox",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# 2. TIMER (Only once!)
# -----------------------------
st_autorefresh(interval=1000, key="timer")

# -----------------------------
# 3. VISIBILITY & STYLE FIXES
# -----------------------------
st.markdown("""
<style>
    /* 1. Main Background (Desktop Wallpaper) */
    .stApp {
        background: url("https://4kwallpapers.com/images/wallpapers/windows-11-stock-official-blue-background-3840x2160-5630.jpg");
        background-size: cover;
        background-attachment: fixed;
    }

    /* 2. Global Text Visibility Fix */
    /* This ensures all standard text, headers, and labels are dark and readable */
    .stMarkdown, p, h1, h2, h3, span, label, .stText {
        color: #ffffff !important;
    }

    /* 3. The Window Container (White box for scenarios) */
    .window-container {
        background: #ffffff !important;
        border-radius: 12px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
        border-top: 35px solid #e2e8f0;
        padding: 30px;
        margin-top: 20px;
    }

    /* 4. Outlook-style Blue Buttons */
    div.stButton > button {
        background-color: #0078D4 !important;
        color: white !important;
        border-radius: 4px !important;
        border: none !important;
        font-weight: 600 !important;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background-color: #005a9e !important;
        border: none !important;
    }

    /* 5. Icons & Labels on the Desktop */
    .icon-box {
        font-size: 55px;
        filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.4));
    }
    .icon-label {
        color: white !important; /* Keep labels white on the blue wallpaper */
        font-weight: 500;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        font-size: 14px;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 4. SESSION STATE
# -----------------------------
if "resilience" not in st.session_state: st.session_state.resilience = 100
if "logs" not in st.session_state: st.session_state.logs = []
if "current_app" not in st.session_state: st.session_state.current_app = None
if "remaining" not in st.session_state: st.session_state.remaining = 180
if "last_update" not in st.session_state: st.session_state.last_update = time.time()
if "completed" not in st.session_state: st.session_state.completed = set()

# Timer Logic
now = time.time()
if (now - st.session_state.last_update) >= 1:
    st.session_state.remaining = max(0, st.session_state.remaining - 1)
    st.session_state.last_update = now

# -----------------------------
# CUSTOM CSS (REACT/MODERN LOOK)
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: url("https://4kwallpapers.com/images/wallpapers/windows-11-stock-official-blue-background-3840x2160-5630.jpg");
        background-size: cover;
    }
    [data-testid="stAppViewContainer"] > .main {
        background: rgba(0, 0, 0, 0.2);
    }
    .desktop-icon {
        text-align: center;
        padding: 15px;
        cursor: pointer;
    }
    .icon-box {
        font-size: 55px;
        filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.4));
    }
    .icon-label {
        color: white;
        font-weight: 500;
        text-shadow: 1px 1px 4px rgba(0,0,0,1);
        font-size: 14px;
        margin-top: 5px;
    }
    .window-container {
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
        border-top: 35px solid #e2e8f0;
        padding: 30px;
        color: #0f172a !important;
        margin-top: 20px;
    }
    .window-container h2, .window-container p, .window-container label {
        color: #0f172a !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# THE 13 SCENARIOS (TRICK QUESTIONS INCLUDED)
# -----------------------------
SCENARIOS = {
    "outlook": {
        "icon": "📧", "title": "Outlook", 
        "desc": "URGENT: Your CEO sent an email asking for 'the secret project files' for a meeting starting in 5 mins. The sender address is 'ceo.office@yourcorp-ltd.com' (your actual domain is @yourcorp.com).",
        "actions": [
            {"l": "Reply with files immediately", "e": -30, "log": "❌ TRICKED: Domain spoofing detected! You sent files to a hacker."},
            {"l": "Call CEO to verify", "e": 15, "log": "✅ VIGILANT: Verified out-of-band. The email was a business compromise attempt."}
        ]
    },
    "mfa": {
        "icon": "🔑", "title": "Authenticator", 
        "desc": "A notification pops up: 'Did you just sign in?'. You were about to log in yourself, but the notification appeared 2 seconds before you finished typing your password.",
        "actions": [
            {"l": "Approve (It's me)", "e": -25, "log": "❌ TRICKED: MFA Fatigue/Timing attack. A hacker was waiting for your login window."},
            {"l": "Deny and Change Password", "e": 15, "log": "✅ SECURE: You spotted the timing discrepancy. Password was likely compromised."}
        ]
    },
    "defender": {
        "icon": "🛡️", "title": "Defender", 
        "desc": "Security Alert: 'Anti-Malware Service Executable' is using 98% of your CPU. A pop-up asks you to 'Kill process to restore system speed'.",
        "actions": [
            {"l": "Kill process", "e": -20, "log": "❌ TRICKED: The pop-up was fake malware. Disabling Defender allowed the payload to run."},
            {"l": "Run Full Offline Scan", "e": 10, "log": "✅ SECURE: You realized a system process wouldn't ask to be killed via pop-up."}
        ]
    },
    "teams": {
        "icon": "💬", "title": "Teams", 
        "desc": "IT Admin 'Mark' messages you: 'We are testing the new firewall. Click this internal link to confirm your workstation is reachable.' Link: 'https://internal-dev-check.io/ping'.",
        "actions": [
            {"l": "Click and confirm", "e": -20, "log": "❌ TRICKED: Shadow IT/Phishing. IT never uses .io domains for internal pings."},
            {"l": "Check IT ticketing portal", "e": 10, "log": "✅ SECURE: You verified if a 'firewall test' was scheduled."}
        ]
    },
    "onedrive": {
        "icon": "📂", "title": "OneDrive", 
        "desc": "You find a folder named 'Confidential_Salaries_2025' shared with 'Everyone'. You are curious and it seems it was shared by mistake.",
        "actions": [
            {"l": "Open to check for errors", "e": -15, "log": "❌ TRICKED: It was a 'Honeypot' file. Opening it alerted the SOC to your unauthorized access."},
            {"l": "Report misconfiguration to IT", "e": 15, "log": "✅ PRO: You followed policy instead of giving in to curiosity."}
        ]
    },
    "wifi": {
        "icon": "📶", "title": "Wi-Fi", 
        "desc": "At a tech conference, 'Conference_Guest_Secure' requires you to install a 'Security Certificate' to access the internet.",
        "actions": [
            {"l": "Install and Connect", "e": -35, "log": "❌ CRITICAL: Installing certificates allows a Man-in-the-Middle to decrypt all your traffic."},
            {"l": "Use Cellular Data", "e": 10, "log": "✅ SECURE: Never trust a network that requires certificate installation."}
        ]
    },
    "usb": {
        "icon": "🔌", "title": "USB Port", 
        "desc": "You find a high-end USB-C charger in the meeting room. Your phone is at 2%.",
        "actions": [
            {"l": "Plug in to charge", "e": -20, "log": "❌ TRICKED: 'O.MG Cable' detected. The charger contained a chip that stole your phone data."},
            {"l": "Ask reception for lost property", "e": 10, "log": "✅ SECURE: Hardware can be weaponized. Only use trusted chargers."}
        ]
    },
    "update": {
        "icon": "⚙️", "title": "Updates", 
        "desc": "A browser tab says: 'Chrome Outdated. Update now to view this content.' and downloads 'Update.dmg' or 'Update.exe' automatically.",
        "actions": [
            {"l": "Run the update", "e": -25, "log": "❌ TRICKED: Browsers update through system settings, not by downloading files from websites."},
            {"l": "Close tab and check settings", "e": 10, "log": "✅ SECURE: You recognized a classic drive-by-download tactic."}
        ]
    },
    "social": {
        "icon": "📱", "title": "Social", 
        "desc": "A recruiter on LinkedIn asks for your work email to send a 'private salary offer' as a PDF. The company looks real.",
        "actions": [
            {"l": "Provide work email", "e": -10, "log": "❌ TRICKED: Targeted Spear-Phishing. Now they have your corporate email for an attack."},
            {"l": "Ask for details on LinkedIn", "e": 5, "log": "✅ VIGILANT: Kept personal and work life separate. Recruiter might be a fake profile."}
        ]
    },
    "backup": {
        "icon": "💾", "title": "Backup", 
        "desc": "Ransomware detected! A message says: 'Pay 1 BTC or we delete everything'. Your last backup was 2 hours ago.",
        "actions": [
            {"l": "Negotiate with hackers", "e": -40, "log": "❌ FAIL: Never negotiate. It marks you as a paying target for future attacks."},
            {"l": "Wipe system and restore", "e": 20, "log": "✅ HERO: Backups saved the day. No money paid, data recovered."}
        ]
    },
    "browser": {
        "icon": "🌐", "title": "Browser", 
        "desc": "Your browser shows 'https://apple.security-check.com'. The padlock is green and the site looks perfect. It asks for your iCloud login.",
        "actions": [
            {"l": "Login to secure account", "e": -25, "log": "❌ TRICKED: Subdomain trickery. The real domain was 'security-check.com', not Apple."},
            {"l": "Type apple.com manually", "e": 15, "log": "✅ SECURE: You ignored the link and went directly to the source."}
        ]
    },
    "cloud": {
        "icon": "☁️", "title": "Cloud Permissions", 
        "desc": "A new AI productivity tool asks for 'Read/Write access to all files' to 'help organize your work'.",
        "actions": [
            {"l": "Grant access", "e": -20, "log": "❌ TRICKED: Over-privileged app. The AI tool was a data scraper in disguise."},
            {"l": "Review Scopes / Deny", "e": 10, "log": "✅ SECURE: Followed the principle of Least Privilege."}
        ]
    },
    "password": {
        "icon": "📝", "title": "Password Policy", 
        "desc": "You need a new password. Which strategy is harder for a modern computer to crack?",
        "actions": [
            {"l": "P@ssw0rd123!", "e": -15, "log": "❌ WEAK: Complexity rules are easy for bots. Length is better."},
            {"l": "purple-elephant-dancing-high", "e": 20, "log": "✅ STRONG: Passphrases have higher entropy and are harder to brute-force."}
        ]
    }
}

# -----------------------------
# STATUS BAR
# -----------------------------
c1, c2, c3 = st.columns([1.5, 2, 1])
with c1:
    st.markdown(f"### ⏳ TIME: {st.session_state.remaining}s")
with c2:
    res_color = "#00ff00" if st.session_state.resilience > 50 else "#ff4b4b"
    st.markdown(f"<h3 style='text-align:center;color:{res_color}'>🛡️ RESILIENCE: {st.session_state.resilience}%</h3>", unsafe_allow_html=True)
with c3:
    if st.button("🏠 DESKTOP", use_container_width=True):
        st.session_state.current_app = None
        st.rerun()

st.progress(max(0, min(int((180 - st.session_state.remaining)/180 * 100), 100)))

# -----------------------------
# GAME OVER LOGIC
# -----------------------------
if st.session_state.resilience <= 0:
    st.error("🚨 CRITICAL BREACH: Your company has been liquidated due to cyber failure.")
    if st.button("REBOOT SYSTEM"):
        st.session_state.clear()
        st.rerun()
    st.stop()

if st.session_state.remaining <= 0:
    st.warning("⏱️ TIME EXPIRED: The audit is over.")
    st.info(f"Final Resilience Score: {st.session_state.resilience}%")
    if st.button("REPLAY"):
        st.session_state.clear()
        st.rerun()
    st.stop()

# -----------------------------
# DESKTOP UI
# -----------------------------
if st.session_state.current_app is None:
    st.write("##")
    cols = st.columns(5)
    
    for i, (key, val) in enumerate(SCENARIOS.items()):
        with cols[i % 5]:
            st.markdown(f"""
                <div class="desktop-icon">
                    <div class="icon-box">{val['icon']}</div>
                    <div class="icon-label">{val['title']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            label = "✅ Done" if key in st.session_state.completed else "Open"
            if st.button(label, key=f"btn_{key}", use_container_width=True):
                st.session_state.current_app = key
                st.rerun()

# -----------------------------
# APP WINDOW (MODAL SIMULATION)
# -----------------------------
else:
    app_id = st.session_state.current_app
    app_data = SCENARIOS[app_id]
    
    st.markdown(f"""
        <div class="window-container">
            <h2 style="margin-top:-10px">{app_data['icon']} {app_data['title']} Task</h2>
            <hr style="border: 0.5px solid #cbd5e1">
            <p style="font-size:18px; line-height:1.6"><b>Challenge:</b> {app_data['desc']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col_a, col_b = st.columns(2)
    for idx, action in enumerate(app_data['actions']):
        with [col_a, col_b][idx]:
            if st.button(action['l'], key=f"act_{idx}", use_container_width=True):
                st.session_state.resilience = max(0, min(100, st.session_state.resilience + action['e']))
                st.session_state.logs.append(action['log'])
                st.session_state.completed.add(app_id)
                st.session_state.current_app = None
                st.rerun()

# -----------------------------
# SYSTEM LOGS
# -----------------------------
st.write("---")
with st.expander("📜 LIVE SECURITY LOGS (SOC)", expanded=True):
    if not st.session_state.logs:
        st.info("Monitoring system... No incidents recorded yet.")
    else:
        for log in reversed(st.session_state.logs[-5:]):
            st.code(log)
