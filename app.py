import streamlit as st
import time

st.set_page_config(
	page_title="Cyber Resilience Sandbox",
	layout="wide",
	initial_sidebar_state="collapsed",
)

st.markdown(
	"""
	<style>
	:root {
		--win11-radius: 14px;
		--win11-radius-sm: 10px;
		--win11-border: rgba(255,255,255,0.18);
		--win11-border-strong: rgba(255,255,255,0.26);
		--win11-acrylic: rgba(18, 18, 20, 0.52);
		--win11-acrylic-strong: rgba(18, 18, 20, 0.66);
		--win11-shadow: 0 18px 45px rgba(0,0,0,0.45);
		--win11-shadow-soft: 0 10px 26px rgba(0,0,0,0.28);
		--win11-text: #f5f7fb;
		--win11-text-dim: rgba(245,247,251,0.78);
		--win11-accent: #0078d4;
	}

	/* Desktop background */
	.stApp {
		background: url("https://4kwallpapers.com/images/wallpapers/windows-11-stock-official-blue-background-3840x2160-5630.jpg");
		background-size: cover;
		background-attachment: fixed;
	}

	/* Acrylic app surface */
	[data-testid="stAppViewContainer"] > .main {
		background: var(--win11-acrylic);
		backdrop-filter: blur(18px) saturate(175%);
		-webkit-backdrop-filter: blur(18px) saturate(175%);
		border-top: 1px solid var(--win11-border);
	}

	/* Windows-like padding */
	[data-testid="stAppViewContainer"] .main {
		padding-top: 1.2rem;
		padding-bottom: 2rem;
	}

	/* Typography: readable on dark */
	html, body, [class*="css"], .stMarkdown, .stText, .stCaption, label, p, li, h1, h2, h3, h4 {
		font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
		color: var(--win11-text) !important;
	}
	.stCaption { color: var(--win11-text-dim) !important; }

	/* Inputs/select: rounded */
	[data-testid="stSelectbox"] > div,
	[data-testid="stTextInput"] > div,
	[data-testid="stTextArea"] > div {
		border-radius: var(--win11-radius-sm) !important;
	}

	/* Main content card */
	.content-container {
		background: rgba(255,255,255,0.92) !important;
		padding: 40px;
		border-radius: var(--win11-radius);
		border: 1px solid rgba(255,255,255,0.55);
		box-shadow: var(--win11-shadow);
		margin-top: 16px;
	}

	/* Dark text inside the white card */
	.content-container, .content-container * {
		color: #141414 !important;
	}

	/* Alerts: ensure readable */
	[data-testid="stAlert"] * { color: #111 !important; }

	/* Buttons: fluent-ish */
	.stButton>button {
		background-color: var(--win11-accent) !important;
		color: white !important;
		border-radius: var(--win11-radius-sm) !important;
		border: 1px solid rgba(255,255,255,0.12) !important;
		height: 3.2em !important;
		font-weight: 600 !important;
		width: 100%;
		box-shadow: 0 10px 20px rgba(0,0,0,0.18);
	}

	/* Status panels */
	.status-panel {
		background: var(--win11-acrylic-strong) !important;
		color: #ffffff !important;
		padding: 18px 20px;
		border-radius: var(--win11-radius);
		text-align: center;
		margin-bottom: 18px;
		border: 1px solid var(--win11-border-strong);
		box-shadow: var(--win11-shadow-soft);
	}

	/* Teams bubble */
	.teams-bubble {
		background: rgba(243, 242, 241, 0.96);
		border-left: 6px solid #6264a7;
		padding: 18px;
		margin: 12px 0;
		border-radius: var(--win11-radius);
		box-shadow: 0 10px 22px rgba(0,0,0,0.12);
	}
	</style>
	""",
	unsafe_allow_html=True,
)

if "resilience" not in st.session_state:
	st.session_state.resilience = 100
if "hacked" not in st.session_state:
	st.session_state.hacked = False
if "start_time" not in st.session_state:
	st.session_state.start_time = time.time()

elapsed = time.time() - st.session_state.start_time
remaining = max(0, int(180 - elapsed))
if remaining == 0:
	st.session_state.hacked = True

col_timer, col_score = st.columns(2)
with col_timer:
	st.markdown(
		f'<div class="status-panel"><h3 style="color:white !important; margin:0;">⏳ TIME: {remaining}s</h3></div>',
		unsafe_allow_html=True,
	)
with col_score:
	st.markdown(
		f'<div class="status-panel"><h3 style="color:white !important; margin:0;">🛡️ RESILIENCE: {st.session_state.resilience}%</h3></div>',
		unsafe_allow_html=True,
	)

if st.session_state.hacked:
	st.markdown(
		"""
		<div style="background-color: #a80000; padding: 100px; border-radius: 15px; text-align: center;">
			<h1 style="color: white !important; margin-bottom: 10px;">🚨 SYSTEM BREACH DETECTED 🚨</h1>
			<p style="color: white !important; font-size: 1.5rem; margin-top: 0;">
				The organization is now under a Ransomware attack.
			</p>
		</div>
		""",
		unsafe_allow_html=True,
	)
	if st.button("SYSTEM RESTORE"):
		st.session_state.resilience = 100
		st.session_state.hacked = False
		st.session_state.start_time = time.time()
		st.rerun()
	st.stop()

app = st.selectbox(
	"Search or Select Application:",
	[
		"📧 Outlook Mail",
		"📂 OneDrive Audit",
		"💬 Teams (Internal Chat)",
		"🛡️ Microsoft Defender",
		"⚙️ System Settings",
	],
	label_visibility="collapsed",
)

st.markdown('<div class="content-container">', unsafe_allow_html=True)

if app == "📧 Outlook Mail":
	st.write("## 📧 Outlook Web - Security Alert")
	st.write("**From:** IT Admin (security-noreply@microsoft-office.net)")
	st.write("**Subject:** Immediate Action: Account Compromise Detected")
	st.info("Technical Analysis: Sender domain uses '.net' instead of '.com'. Link points to a URL shortener.")

	col1, col2 = st.columns(2)
	if col1.button("Verify Identity Now", key="outlook_verify"):
		st.session_state.resilience = max(0, st.session_state.resilience - 40)
		st.error("❌ PHISHED! You entered credentials on a fake site. Domain '.net' was a trap.")
	if col2.button("Report as Phishing", key="outlook_report"):
		st.session_state.resilience = min(100, st.session_state.resilience + 20)
		st.success("🎯 Correct! You identified the spoofed domain.")

elif app == "💬 Teams (Internal Chat)":
	st.write("## 💬 Microsoft Teams - New Chat")
	st.markdown(
		"""
		<div class="teams-bubble">
			<b>External (IT Support - Mark):</b><br><br>
			Hi Serena, I'm verifying your account migration. I've sent a 6-digit MFA code to your phone.
			Can you please share it here to complete the process?
		</div>
		""",
		unsafe_allow_html=True,
	)
	col_a, col_b = st.columns(2)
	if col_a.button("Share MFA Code", key="teams_share_mfa"):
		st.session_state.hacked = True
		st.rerun()
	if col_b.button("Refuse & Report User", key="teams_refuse"):
		st.session_state.resilience = min(100, st.session_state.resilience + 30)
		st.success("🏆 PROTECTED! IT will NEVER ask for MFA codes via chat. This was Social Engineering.")

elif app == "📂 OneDrive Audit":
	st.write("## 📂 OneDrive - Sharing Review")
	st.write("The following critical folders are currently shared with **'Anyone with the link'**:")
	folders = [
		["Financial_Report_2025.zip", "Public"],
		["Employee_IDs.pdf", "Public"],
	]
	for name, visibility in folders:
		c1, c2 = st.columns([3, 1])
		c1.write(f"⚠️ **{name}** | Risk: High Exposure | Current: {visibility}")
		if c2.button("Make Private", key=f"onedrive_private_{name}"):
			st.session_state.resilience = min(100, st.session_state.resilience + 10)
			st.success(f"Permission revoked for {name}!")

elif app == "🛡️ Microsoft Defender":
	st.write("## 🛡️ Windows Security Center")
	st.warning("New Hardware: Unknown USB drive detected (Label: 'BACKUP_DRIVE')")
	st.write("Background: You found this drive in the coffee area. What is your action?")
	colx, coly = st.columns(2)
	if colx.button("Open Folder to Identify Owner", key="defender_open_usb"):
		st.session_state.resilience = max(0, st.session_state.resilience - 50)
		st.error("🚨 MALWARE! The drive contained a 'Rubber Ducky' script. Keystrokes are being recorded.")
	if coly.button("Deliver to IT Security", key="defender_deliver_usb"):
		st.session_state.resilience = min(100, st.session_state.resilience + 20)
		st.success("✅ SMART: Plugging in unknown USBs is a critical security violation.")

elif app == "⚙️ System Settings":
	st.write("## ⚙️ Settings - Installed Apps")
	st.write("Shadow IT Detection: Identify and remove unauthorized software.")
	soft = [
		["Microsoft Office", "Safe"],
		["Free-VPN-Pro (Unsigned)", "Risk"],
		["Advanced_Web_Crawler.exe", "Risk"],
	]
	for app_name, status in soft:
		ca, cb = st.columns([3, 1])
		ca.write(f"**{app_name}** | Status: {status}")
		if status == "Risk":
			if cb.button("Uninstall", key=f"uninstall_{app_name}"):
				st.session_state.resilience = min(100, st.session_state.resilience + 15)
				st.success(f"App removed: {app_name}")

st.markdown("</div>", unsafe_allow_html=True)
