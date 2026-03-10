import streamlit as st
import time
import random
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# CONFIGURAZIONE PAGINA
# -----------------------------
st.set_page_config(
    page_title="Cyber Resilience Sandbox",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Refresh ogni secondo per il timer
st_autorefresh(interval=1000, key="timer")

# -----------------------------
# SESSION STATE
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
# CSS CUSTOM (STILE REACT-LIKE)
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
    /* Barra di stato superiore */
    .status-bar {
        background: rgba(15, 23, 42, 0.9);
        padding: 15px;
        border-radius: 0 0 15px 15px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }
    /* Icone Desktop */
    .desktop-icon {
        text-align: center;
        padding: 15px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .icon-box {
        font-size: 50px;
        margin-bottom: 5px;
        filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));
    }
    .icon-label {
        color: white;
        font-weight: 500;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.8);
        font-size: 14px;
    }
    /* Finestra App (Modale) */
    .window-container {
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        border-top: 35px solid #f1f5f9;
        position: relative;
        padding: 30px;
        color: #1e293b !important;
        margin-top: 20px;
    }
    .window-container h3, .window-container p {
        color: #1e293b !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DATA: I 13 SCENARI
# -----------------------------
SCENARIOS = {
    "outlook": {"icon": "📧", "title": "Outlook", "desc": "Email sospetta: 'Vincita iPhone 15! Clicca qui.'", "actions": [{"l": "Clicca link", "e": -20, "log": "❌ Cliccato link phishing"}, {"l": "Segnala", "e": 5, "log": "✅ Segnalato phishing"}]},
    "defender": {"icon": "🛡️", "title": "Defender", "desc": "Rilevato 'setup_premium.exe' nei Download.", "actions": [{"l": "Esegui", "e": -15, "log": "❌ Malware eseguito"}, {"l": "Quarantena", "e": 10, "log": "✅ Minaccia isolata"}]},
    "mfa": {"icon": "🔑", "title": "MFA", "desc": "Richiesta login da IP sconosciuto (Russia).", "actions": [{"l": "Approva", "e": -25, "log": "❌ Accesso illecito approvato"}, {"l": "Nega", "e": 10, "log": "✅ Intrusione bloccata"}]},
    "teams": {"icon": "💬", "title": "Teams", "desc": "Un collega chiede il tuo codice OTP via chat.", "actions": [{"l": "Invia codice", "e": -30, "log": "❌ Social Engineering riuscito"}, {"l": "Segnala utente", "e": 15, "log": "✅ Segnalato account compromesso"}]},
    "onedrive": {"icon": "📂", "title": "OneDrive", "desc": "Rilevato download massivo di file aziendali.", "actions": [{"l": "Ignora", "e": -20, "log": "❌ Esfiltrazione dati in corso"}, {"l": "Blocca utente", "e": 15, "log": "✅ Data Loss Prevention attiva"}]},
    "wifi": {"icon": "📶", "title": "Wi-Fi", "desc": "Ti trovi in aeroporto. C'è una rete 'Free_Public_WiFi'.", "actions": [{"l": "Connetti", "e": -15, "log": "❌ Man-in-the-middle risk"}, {"l": "Usa Hotspot 4G", "e": 10, "log": "✅ Connessione sicura"}]},
    "update": {"icon": "⚙️", "title": "Updates", "desc": "Patch di sicurezza critica disponibile per Windows.", "actions": [{"l": "Rimanda", "e": -10, "log": "❌ Sistema vulnerabile"}, {"l": "Aggiorna ora", "e": 10, "log": "✅ Sistema patchato"}]},
    "usb": {"icon": "🔌", "title": "USB Scan", "desc": "Trovata chiavetta USB nel parcheggio aziendale.", "actions": [{"l": "Inserisci", "e": -25, "log": "❌ Attacco 'BadUSB' eseguito"}, {"l": "Consegna a IT", "e": 10, "log": "✅ Protocollo sicurezza seguito"}]},
    "social": {"icon": "📱", "title": "Social", "desc": "Richiesta d'amicizia da un recruiter sospetto su LinkedIn.", "actions": [{"l": "Accetta", "e": -10, "log": "❌ Raccolta info (OSINT)"}, {"l": "Ignora", "e": 5, "log": "✅ Privacy protetta"}]},
    "backup": {"icon": "💾", "title": "Backup", "desc": "Il sistema chiede di verificare l'integrità dei backup.", "actions": [{"l": "Salta", "e": -15, "log": "❌ Rischio perdita dati"}, {"l": "Verifica", "e": 10, "log": "✅ Ripristino garantito"}]},
    "browser": {"icon": "🌐", "title": "Browser", "desc": "Il browser segnala un certificato SSL scaduto.", "actions": [{"l": "Procedi comunque", "e": -15, "log": "❌ Navigazione non sicura"}, {"l": "Esci dal sito", "e": 5, "log": "✅ Evitato sito sospetto"}]},
    "cloud": {"icon": "☁️", "title": "Cloud App", "desc": "Un'app esterna chiede permessi di lettura sulla tua mail.", "actions": [{"l": "Autorizza", "e": -20, "log": "❌ Accesso dati non autorizzato"}, {"l": "Nega permessi", "e": 10, "log": "✅ Shadow IT bloccato"}]},
    "password": {"icon": "📝", "title": "Policy", "desc": "Devi scegliere una nuova password aziendale.", "actions": [{"l": "User2024!", "e": -10, "log": "❌ Password debole"}, {"l": "K9#m$P2!zQ", "e": 15, "log": "✅ Password robusta"}]}
}

# -----------------------------
# HEADER (STATUS BAR)
# -----------------------------
c1, c2, c3 = st.columns([1.5, 2, 1])
with c1:
    st.markdown(f"### ⏳ {st.session_state.remaining}s")
with c2:
    color = "#00ff00" if st.session_state.resilience > 50 else "#ff4b4b"
    st.markdown(f"<h3 style='text-align:center;color:{color}'>🛡️ RESILIENZA: {st.session_state.resilience}%</h3>", unsafe_allow_html=True)
with c3:
    if st.button("🏠 DESKTOP", use_container_width=True):
        st.session_state.current_app = None
        st.rerun()

st.progress(max(0, min(int((180 - st.session_state.remaining)/180 * 100), 100)))

# -----------------------------
# CONTROLLO FINE GIOCO
# -----------------------------
if st.session_state.resilience <= 0 or st.session_state.remaining <= 0:
    st.error("🚨 SISTEMA COMPROMESSO! Ransomware attivo.")
    if st.button("RESTART"):
        st.session_state.clear()
        st.rerun()
    st.stop()

# -----------------------------
# DESKTOP GRID (Se nessuna app aperta)
# -----------------------------
if st.session_state.current_app is None:
    st.write("##")
    cols = st.columns(5) # Griglia da 5 icone per riga
    
    for i, (key, val) in enumerate(SCENARIOS.items()):
        with cols[i % 5]:
            st.markdown(f"""
                <div class="desktop-icon">
                    <div class="icon-box">{val['icon']}</div>
                    <div class="icon-label">{val['title']}</div>
                </div>
            """, unsafe_allow_html=True)
            # Determina se l'app è già stata completata
            btn_label = "✅ Fatto" if key in st.session_state.completed else "Apri"
            if st.button(btn_label, key=f"btn_{key}", use_container_width=True):
                st.session_state.current_app = key
                st.rerun()

# -----------------------------
# APP WINDOW (Se un'app è aperta)
# -----------------------------
else:
    app_id = st.session_state.current_app
    app_data = SCENARIOS[app_id]
    
    st.markdown(f"""
        <div class="window-container">
            <h2 style="margin-top:-10px">{app_data['icon']} {app_data['title']}</h2>
            <hr>
            <p style="font-size:18px">{app_data['desc']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Pulsanti azioni (fuori dal markdown per funzionare)
    col_act1, col_act2 = st.columns(2)
    for idx, action in enumerate(app_data['actions']):
        with [col_act1, col_act2][idx]:
            if st.button(action['l'], key=f"act_{idx}", use_container_width=True):
                st.session_state.resilience = max(0, min(100, st.session_state.resilience + action['e']))
                st.session_state.logs.append(action['log'])
                st.session_state.completed.add(app_id)
                st.session_state.current_app = None # Torna al desktop
                st.rerun()

# -----------------------------
# LOGS (SOC PANEL)
# -----------------------------
st.write("---")
with st.expander("📜 SYSTEM LOGS (Security Operations Center)", expanded=True):
    if not st.session_state.logs:
        st.info("In attesa di eventi...")
    else:
        for log in reversed(st.session_state.logs[-5:]):
            st.code(log)
