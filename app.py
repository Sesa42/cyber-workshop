import streamlit as st
import time
import random
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Cyber Resilience Mega Sandbox",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st_autorefresh(interval=1000, key="timer")

# -----------------------------
# CSS STYLE (Desktop Edition)
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: url("https://4kwallpapers.com/images/wallpapers/windows-11-stock-official-blue-background-3840x2160-5630.jpg");
        background-size: cover;
    }
    [data-testid="stAppViewContainer"] > .main {
        background: rgba(0, 0, 0, 0.3);
    }
    /* Stile Icone Desktop */
    .desktop-icon-container {
        text-align: center;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .desktop-icon-container:hover {
        transform: scale(1.1);
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    .icon-text {
        color: white;
        font-size: 14px;
        text-shadow: 1px 1px 3px black;
        margin-top: 5px;
    }
    /* Finestra App */
    .window-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 25px;
        color: #1a1a1a !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        border-top: 30px solid #e0e0e0; /* Simula barra titolo */
        position: relative;
    }
    .window-container * { color: #1a1a1a !important; }
    
    .status-panel {
        background: rgba(0,0,0,0.6);
        padding: 10px;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "resilience" not in st.session_state: st.session_state.resilience = 100
if "logs" not in st.session_state: st.session_state.logs = []
if "current_app" not in st.session_state: st.session_state.current_app = None # Nessuna app aperta all'inizio
if "remaining" not in st.session_state: st.session_state.remaining = 180
if "last_update" not in st.session_state: st.session_state.last_update = time.time()

# Timer Logic
now = time.time()
if (now - st.session_state.last_update) >= 1:
    st.session_state.remaining = max(0, st.session_state.remaining - 1)
    st.session_state.last_update = now

# -----------------------------
# TOP BAR (Status)
# -----------------------------
c1, c2, c3 = st.columns([2, 2, 1])
with c1:
    st.markdown(f'<div class="status-panel"><h4 style="color:white;margin:0;">⏳ TEMPO: {st.session_state.remaining}s</h4></div>', unsafe_allow_html=True)
with c2:
    color = "#00ff00" if st.session_state.resilience > 50 else "#ff4b4b"
    st.markdown(f'<div class="status-panel"><h4 style="color:white;margin:0;">🛡️ SICUREZZA: <span style="color:{color};">{st.session_state.resilience}%</span></h4></div>', unsafe_allow_html=True)
with c3:
    if st.button("🏠 DESKTOP"):
        st.session_state.current_app = None
        st.rerun()

st.progress(int((180 - st.session_state.remaining)/180 * 100))

# -----------------------------
# DESKTOP ICONS (Visualizzate solo se nessuna app è aperta)
# -----------------------------
if st.session_state.current_app is None:
    st.write("##") # Spazio superiore
    col_ic1, col_ic2, col_ic3, col_ic4 = st.columns(4)
    
    with col_ic1:
        st.markdown('<div class="desktop-icon-container"><h1>📧</h1><p class="icon-text">Outlook</p></div>', unsafe_allow_html=True)
        if st.button("Apri Outlook", key="btn_mail"): 
            st.session_state.current_app = "Outlook"
            st.rerun()

    with col_ic2:
        st.markdown('<div class="desktop-icon-container"><h1>🛡️</h1><p class="icon-text">Defender</p></div>', unsafe_allow_html=True)
        if st.button("Apri Defender", key="btn_def"): 
            st.session_state.current_app = "Defender"
            st.rerun()

    with col_ic3:
        st.markdown('<div class="desktop-icon-container"><h1>🔑</h1><p class="icon-text">MFA</p></div>', unsafe_allow_html=True)
        if st.button("Apri MFA", key="btn_mfa"): 
            st.session_state.current_app = "MFA"
            st.rerun()

    with col_ic4:
        st.markdown('<div class="desktop-icon-container"><h1>🎯</h1><p class="icon-text">Quiz</p></div>', unsafe_allow_html=True)
        if st.button("Apri Quiz", key="btn_quiz"): 
            st.session_state.current_app = "Quiz"
            st.rerun()

# -----------------------------
# APP WINDOW (Visualizzata solo se un'app è selezionata)
# -----------------------------
else:
    st.markdown('<div class="window-container">', unsafe_allow_html=True)
    
    curr = st.session_state.current_app
    
    if curr == "Outlook":
        st.subheader("📧 Outlook Web App")
        st.write("Hai ricevuto un'email sospetta: *'Vincita iPhone 15!'*")
        if st.button("Clicca sul link"):
            st.session_state.resilience -= 20
            st.session_state.logs.append("❌ Errore: Cliccato link malevolo")
            st.rerun()
        if st.button("Segnala come Phishing"):
            st.session_state.resilience = min(100, st.session_state.resilience + 5)
            st.session_state.logs.append("✅ Successo: Phishing segnalato")
            st.rerun()

    elif curr == "Defender":
        st.subheader("🛡️ Windows Defender")
        st.write("Stato scansione: 1 minaccia potenziale trovata.")
        if st.button("Quarantena File"):
            st.session_state.resilience = min(100, st.session_state.resilience + 10)
            st.session_state.logs.append("✅ Defender: Trojan rimosso")
            st.rerun()

    elif curr == "MFA":
        st.subheader("🔑 Microsoft Authenticator")
        st.warning("Richiesta di login da Pechino (IP: 103.x.x.x)")
        if st.button("NEGA ACCESSO"):
            st.session_state.resilience = min(100, st.session_state.resilience + 15)
            st.session_state.logs.append("✅ MFA: Attacco respinto")
            st.rerun()

    elif curr == "Quiz":
        st.subheader("🎯 Security Awareness Quiz")
        ans = st.radio("Qual è la password più sicura?", ["123456", "Password!", "C4v4ll0_B14nc0!"])
        if st.button("Invia Risposta"):
            if ans == "C4v4ll0_B14nc0!":
                st.session_state.resilience = min(100, st.session_state.resilience + 10)
                st.success("Ottimo!")
            else:
                st.session_state.resilience -= 10
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# LOGS
# -----------------------------
st.write("---")
with st.expander("📜 Visualizza Log di Sistema (SOC)"):
    for log in reversed(st.session_state.logs[-5:]):
        st.write(log)
