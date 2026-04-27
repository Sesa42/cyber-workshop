import streamlit as st
import time
import random  #
from streamlit_autorefresh import st_autorefresh
# Updated app.py

# ========================================
# CONSTANTS & CONFIGURATION
# ========================================
TOTAL_TIME = 180  # Total time in seconds
MAX_RESILIENCE = 100
MIN_RESILIENCE = 0
RESILIENCE_WARNING_THRESHOLD = 50
COLUMNS_PER_ROW = 5
LOG_DISPLAY_COUNT = 5
# Fixing the truncated Outlook email description

# Background image URL
BG_IMAGE_URL = "https://4kwallpapers.com/images/wallpapers/windows-11-stock-official-blue-background-3840x2160-5630.jpg"

# ========================================
# PAGE CONFIGURATION
# ========================================
st.set_page_config(
    page_title="Cyber Resilience Sandbox",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Auto-refresh every second
st_autorefresh(interval=1000, key="timer")

# ========================================
# UNIFIED STYLING
# ========================================
def apply_styles() -> None:
    """Apply all CSS styling for the application."""
    st.markdown(f"""
    <style>
        /* Sfondo principale */
        .stApp {{
            background: url("{BG_IMAGE_URL}");
            background-size: cover;
            background-attachment: fixed;
        }}

        /* CLASSE PER TESTO SU DESKTOP (Icone e Timer) */
        .desktop-text {{
            color: #ffffff !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            font-weight: 600;
        }}

        /* CLASSE PER TESTO DENTRO LE FINESTRE (Task) */
        .window-text {{
            color: #0f172a !important;
        }}

        /* FINESTRA TASK */
        .window-container {{
            background: rgba(255, 255, 255, 0.98) !important;
            border-radius: 12px;
            padding: 25px;
            border-top: 35px solid #e2e8f0;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }}

        /* LIVE LOGS (SOC) */
        .stExpander {{
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 8px !important;
        }}
        
        /* FIX: Rende i log scorrevoli se diventano troppi */
        .stExpander div[role="ant-design-pro-layout"] {{
            max-height: 300px;
            overflow-y: auto;
        }}

        .log-entry {{
            color: #1e293b !important;
            font-family: 'Courier New', Courier, monospace;
            background: #f1f5f9;
            padding: 8px;
            border-radius: 4px;
            margin-bottom: 5px;
            border-left: 4px solid #0078D4;
        }}

        /* Bottoni */
        div.stButton > button {{
            background-color: #0078D4 !important;
            color: white !important;
            font-weight: 600 !important;
        }}
    </style>
    """, unsafe_allow_html=True)
# ========================================
# SESSION STATE INITIALIZATION
# ========================================
def init_session_state() -> None:
    """Initialize all session state variables with defaults."""
    defaults = {
        "resilience": MAX_RESILIENCE,
        "logs": [],
        "current_app": None,
        "remaining": TOTAL_TIME,
        "last_update": time.time(),
        "completed": set(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ========================================
# TIMER LOGIC
# ========================================
def update_timer() -> None:
    """Update the remaining time every second."""
    now = time.time()
    if (now - st.session_state.last_update) >= 1:
        st.session_state.remaining = max(0, st.session_state.remaining - 1)
        st.session_state.last_update = now

# ========================================
# THE 13 SCENARIOS
# ========================================
SCENARIOS = {
    "outlook": {
        "icon": "📧",
        "title": "Outlook",
        "desc": "URGENT: Your CEO sent an email asking for 'the secret project files' for a meeting starting in 5 mins. The sender address is 'ceo.office@yourcorp-ltd.com' (your actual domain is yourcorp.com). What do you do?",
        "actions": [
            {"l": "Reply with files immediately", "e": -30, "log": "❌ TRICKED: Domain spoofing detected! You sent files to a hacker."},
            {"l": "Call CEO to verify", "e": 15, "log": "✅ VIGILANT: Verified out-of-band. The email was a business compromise attempt."},
        ],
    },
    "mfa": {
        "icon": "🔑",
        "title": "Authenticator",
        "desc": "A notification pops up: 'Did you just sign in?'. You were about to log in yourself, but the notification appeared 2 seconds before you finished typing your password.",
        "actions": [
            {"l": "Approve (It's me)", "e": -25, "log": "❌ TRICKED: MFA Fatigue/Timing attack. A hacker was waiting for your login window."},
            {"l": "Deny and Change Password", "e": 15, "log": "✅ SECURE: You spotted the timing discrepancy. Password was likely compromised."},
        ],
    },
    "defender": {
        "icon": "🛡️",
        "title": "Defender",
        "desc": "Security Alert: 'Anti-Malware Service Executable' is using 98% of your CPU. A pop-up asks you to 'Kill process to restore system speed'.",
        "actions": [
            {"l": "Kill process", "e": -20, "log": "❌ TRICKED: The pop-up was fake malware. Disabling Defender allowed the payload to run."},
            {"l": "Run Full Offline Scan", "e": 10, "log": "✅ SECURE: You realized a system process wouldn't ask to be killed via pop-up."},
        ],
    },
    "teams": {
        "icon": "👥",
        "title": "Teams",
        "desc": "IT Admin 'Mark' messages you: 'We are testing the new firewall. Click this internal link to confirm your workstation is reachable.' Link: 'https://internal-dev-check.io/ping'.",
        "actions": [
            {"l": "Click and confirm", "e": -20, "log": "❌ TRICKED: Shadow IT/Phishing. IT never uses .io domains for internal pings."},
            {"l": "Check IT ticketing portal", "e": 10, "log": "✅ SECURE: You verified if a 'firewall test' was scheduled."},
        ],
    },
    "onedrive": {
        "icon": "📂",
        "title": "OneDrive",
        "desc": "You find a folder named 'Confidential_Salaries_2025' shared with 'Everyone'. You are curious and it seems it was shared by mistake.",
        "actions": [
            {"l": "Open to check for errors", "e": -15, "log": "❌ TRICKED: It was a 'Honeypot' file. Opening it alerted the SOC to your unauthorized access."},
            {"l": "Report misconfiguration to IT", "e": 15, "log": "✅ PRO: You followed policy instead of giving in to curiosity."},
        ],
    },
    "wifi": {
        "icon": "📶",
        "title": "Wi-Fi",
        "desc": "At a tech conference, 'Conference_Guest_Secure' requires you to install a 'Security Certificate' to access the internet.",
        "actions": [
            {"l": "Install and Connect", "e": -35, "log": "❌ CRITICAL: Installing certificates allows a Man-in-the-Middle to decrypt all your traffic."},
            {"l": "Use Cellular Data", "e": 10, "log": "✅ SECURE: Never trust a network that requires certificate installation."},
        ],
    },
    "usb": {
        "icon": "🔌",
        "title": "USB Port",
        "desc": "You find a high-end USB-C charger in the meeting room. Your phone is at 2%.",
        "actions": [
            {"l": "Plug in to charge", "e": -20, "log": "❌ TRICKED: 'O.MG Cable' detected. The charger contained a chip that stole your phone data."},
            {"l": "Ask reception for lost property", "e": 10, "log": "✅ SECURE: Hardware can be weaponized. Only use trusted chargers."},
        ],
    },
    "update": {
        "icon": "🔁",
        "title": "Updates",
        "desc": "A browser tab says: 'Chrome Outdated. Update now to view this content.' and downloads 'Update.dmg' or 'Update.exe' automatically.",
        "actions": [
            {"l": "Run the update", "e": -25, "log": "❌ TRICKED: Browsers update through system settings, not by downloading files from websites."},
            {"l": "Close tab and check settings", "e": 10, "log": "✅ SECURE: You recognized a classic drive-by-download tactic."},
        ],
    },
    "social": {
        "icon": "📱",
        "title": "Social",
        "desc": "A recruiter on LinkedIn asks for your work email to send a 'private salary offer' as a PDF. The company looks real.",
        "actions": [
            {"l": "Provide work email", "e": -10, "log": "❌ TRICKED: Targeted Spear-Phishing. Now they have your corporate email for an attack."},
            {"l": "Ask for details on LinkedIn", "e": 5, "log": "✅ VIGILANT: Kept personal and work life separate. Recruiter might be a fake profile."},
        ],
    },
    "backup": {
        "icon": "💾",
        "title": "Backup",
        "desc": "Ransomware detected! A message says: 'Pay 1 BTC or we delete everything'. Your last backup was 2 hours ago.",
        "actions": [
            {"l": "Negotiate with hackers", "e": -40, "log": "❌ FAIL: Never negotiate. It marks you as a paying target for future attacks."},
            {"l": "Wipe system and restore", "e": 20, "log": "✅ HERO: Backups saved the day. No money paid, data recovered."},
        ],
    },
    "browser": {
        "icon": "🌐",
        "title": "Browser",
        "desc": "Your browser shows 'https://apple.security-check.com'. The padlock is green and the site looks perfect. It asks for your iCloud login.",
        "actions": [
            {"l": "Login to secure account", "e": -25, "log": "❌ TRICKED: Subdomain trickery. The real domain was 'security-check.com', not Apple."},
            {"l": "Type apple.com manually", "e": 15, "log": "✅ SECURE: You ignored the link and went directly to the source."},
        ],
    },
    "cloud": {
        "icon": "☁️",
        "title": "Cloud Permissions",
        "desc": "A new AI productivity tool asks for 'Read/Write access to all files' to 'help organize your work'.",
        "actions": [
            {"l": "Grant access", "e": -20, "log": "❌ TRICKED: Over-privileged app. The AI tool was a data scraper in disguise."},
            {"l": "Review Scopes / Deny", "e": 10, "log": "✅ SECURE: Followed the principle of Least Privilege."},
        ],
    },
    "password": {
        "icon": "🔐",
        "title": "Password Policy",
        "desc": "You need a new password. Which strategy is harder for a modern computer to crack?",
        "actions": [
            {"l": "P@ssw0rd123!", "e": -15, "log": "❌ WEAK: Complexity rules are easy for bots. Length is better."},
            {"l": "purple-elephant-dancing-high", "e": 20, "log": "✅ STRONG: Passphrases have higher entropy and are harder to brute-force."},
        ],
    },
}

# ========================================
# MAIN APPLICATION LOGIC
# ========================================

# 1. Inizializzazione
init_session_state()
update_timer()
apply_styles()

# 2. Controllo Stato Finale
all_tasks_done = len(st.session_state.completed) == len(SCENARIOS)
game_finished = st.session_state.remaining <= 0 or all_tasks_done
is_dead = st.session_state.resilience <= MIN_RESILIENCE

# --- SCENARIO A: VISUALIZZAZIONE RISULTATI (Audit Finale) ---
if game_finished or is_dead:
    if st.session_state.resilience > RESILIENCE_WARNING_THRESHOLD and not is_dead:
        st.balloons()

    st.markdown('<div class="window-container"><h1 class="window-text" style="text-align:center;">📊 AUDIT DI SICUREZZA COMPLETATO</h1></div>', unsafe_allow_html=True)

    c_res, c_task = st.columns(2)
    with c_res:
        passed = st.session_state.resilience > RESILIENCE_WARNING_THRESHOLD and not is_dead
        res_status = "PASSED ✅" if passed else "FAILED ❌"
        res_color = "#00ff00" if passed else "#ff4b4b"
        st.markdown(f"""
            <div style='text-align:center; background:rgba(255,255,255,0.1); padding:20px; border-radius:15px;'>
                <h2 class='window-text'>Risultato</h2>
                <h1 style='color:{res_color}; font-size:48px;'>{res_status}</h1>
                <h3 class='window-text'>Resilienza Finale: {st.session_state.resilience}%</h3>
            </div>
        """, unsafe_allow_html=True)

    with c_task:
        perc = int(len(st.session_state.completed) / len(SCENARIOS) * 100)
        st.markdown(f"""
            <div style='text-align:center; background:rgba(255,255,255,0.1); padding:20px; border-radius:15px;'>
                <h2 class='window-text'>Copertura Task</h2>
                <h1 class='window-text' style='font-size:48px;'>{perc}%</h1>
                <h3 class='window-text'>{len(st.session_state.completed)}/13 Scenari Gestiti</h3>
            </div>
        """, unsafe_allow_html=True)

    st.write("##")
    st.write("### 📝 Sommario Attività (Blackbox Audit Log)")
    for log in reversed(st.session_state.logs):
        st.markdown(f"<div class='log-entry'>{log}</div>", unsafe_allow_html=True)

    st.write("---")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 RIAVVIA WORKSHOP", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    with col_btn2:
        log_text = "\n".join(st.session_state.logs)
        st.download_button("📥 SCARICA REPORT TXT", log_text, "audit_report.txt", use_container_width=True)

    st.stop()  # CRITICO: Ferma l'esecuzione qui per non disegnare il desktop sotto i risultati

# --- SCENARIO B: GIOCO IN CORSO (DESKTOP UI) ---

# 1. Barra di Stato Superiore
c1, c2, c3 = st.columns([1.5, 2, 1])
with c1:
    st.markdown(f"""
        <div class='desktop-text' style='background: rgba(0,0,0,0.4); padding: 10px; border-radius: 10px; font-size: 24px; font-weight: bold; text-align: center;'>
            ⏳ TIME: {st.session_state.remaining}s
        </div>
    """, unsafe_allow_html=True)

with c2:
    curr_res = st.session_state.resilience
    color = "#00ff00" if curr_res > RESILIENCE_WARNING_THRESHOLD else "#ff4b4b"
    st.markdown(f"<h3 style='text-align:center;color:{color}'>🛡️ RESILIENCE: {curr_res}%</h3>", unsafe_allow_html=True)

with c3:
    if st.button("🏠 DESKTOP", use_container_width=True):
        st.session_state.current_app = None
        st.rerun()

# 2. Barra di Avanzamento Temporale
progress_value = max(0, min(int((TOTAL_TIME - st.session_state.remaining) / TOTAL_TIME * 100), 100))
st.progress(progress_value)

# 3. Renderizzazione Contenuto Principale
if st.session_state.current_app is None:
    # Mostra Desktop con icone
    st.write("##")
    cols = st.columns(COLUMNS_PER_ROW)
    for i, (key, val) in enumerate(SCENARIOS.items()):
        with cols[i % COLUMNS_PER_ROW]:
            st.markdown(f"""
                <div style='text-align:center; margin-bottom:10px;'>
                    <div style='font-size:50px;'>{val['icon']}</div>
                    <div class='desktop-text'>{val['title']}</div>
                </div>
            """, unsafe_allow_html=True)

            btn_label = "✅ Done" if key in st.session_state.completed else "Open"
            if st.button(btn_label, key=f"btn_{key}", use_container_width=True):
                st.session_state.current_app = key
                st.rerun()
else:
    # Mostra Finestra della Task attiva
    app_id = st.session_state.current_app
    app_data = SCENARIOS[app_id]
    st.markdown(f"""
    <div class="window-container">
        <h2 class="window-text" style="margin-top:-10px">{app_data['icon']} {app_data['title']} Task</h2>
        <hr>
        <p class="window-text" style="font-size:18px;"><b>Challenge:</b> {app_data['desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    # Logica Randomizzazione Risposte
    action_indices = list(range(len(app_data["actions"])))
    random.seed(st.session_state.current_app)
    random.shuffle(action_indices)

    for i, idx in enumerate(action_indices):
        action = app_data["actions"][idx]
        with [col_a, col_b][i]:
            if st.button(action["l"], key=f"act_{app_id}_{idx}", use_container_width=True):
                st.session_state.resilience = max(0, min(100, st.session_state.resilience + action["e"]))
                st.session_state.logs.append(action["log"])
                st.session_state.completed.add(app_id)
                st.session_state.current_app = None
                random.seed()  # Reset seed
                st.rerun()

# 4. Expander dei Log SOC (Sempre visibile durante il gioco)
st.write("---")
with st.expander("📜 LIVE SECURITY LOGS (SOC)", expanded=True):
    if not st.session_state.logs:
        st.info("Sistema in monitoraggio... Nessun incidente rilevato.")
    else:
        for log in reversed(st.session_state.logs):
            st.markdown(f"<div class='log-entry'>**LOG:** {log}</div>", unsafe_allow_html=True)

# 5. Bottone di Download (Sempre disponibile a fondo pagina)
if st.session_state.logs:
    log_report = "\n".join(st.session_state.logs)
    st.download_button(
        label="📥 Scarica Report Sicurezza (TXT)",
        data=log_report,
        file_name="cyber_audit_report.txt",
        mime="text/plain"
    )
