import streamlit as st
import time
import datetime
from autohunter_core import normalize_target, load_proxies, RequestEngine, BlockDetected
from wrappers import AVAILABLE_MODULES

# 1. Page Configuration & Hacker CSS
st.set_page_config(page_title="AUTOHUNTER // OFFENSIVE", page_icon="💀", layout="wide")

st.markdown("""
<style>
    /* Dark Theme */
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #00ff41; }
    /* Buttons */
    .stButton>button { background-color: #000; color: #00ff41; border: 1px solid #00ff41; border-radius: 0; font-weight: bold; transition: 0.3s; width: 100%; }
    .stButton>button:hover { background-color: #00ff41; color: #000; box-shadow: 0 0 10px #00ff41; }
    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #111; color: #00ff41; border: 1px solid #333; border-radius: 0; }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus { border-color: #00ff41; box-shadow: 0 0 5px #00ff41; }
    /* Typography */
    h1, h2, h3 { color: #ff003c !important; text-transform: uppercase; letter-spacing: 2px; }
    p, label { color: #00ff41 !important; }
</style>
""", unsafe_allow_html=True)

st.title("💀 AUTOHUNTER // v2.0")
st.markdown("`[ SYSTEM READY ]` // Awaiting target parameters...")

# Initialize Session State for Engine to persist across reruns
if 'engine' not in st.session_state:
    st.session_state.engine = RequestEngine()
if 'proxy_index' not in st.session_state:
    st.session_state.proxy_index = 0

# Sidebar Settings
with st.sidebar:
    st.header("[ CONFIGURATION ]")
    target_input = st.text_input("TARGET (Domain/IP)", "http://127.0.0.1:8002/xss?q=test", key="target_input")
    
    st.subheader("[ MODULES ]")
    selected_modules = []
    for mod_name in AVAILABLE_MODULES.keys():
        # پیش‌فرض تیک‌ها خاموش است تا خودت انتخاب کنی
        if st.checkbox(mod_name, value=False, key=f"chk_{mod_name}"):
            selected_modules.append(mod_name)
    
    st.subheader("[ EVASION ]")
    use_proxy = st.checkbox("Enable Proxy Rotation", key="chk_proxy")
    proxy_text = st.text_area("Proxy List (one per line)", placeholder="http://ip:port", key="proxy_text")
    
    if st.button("🔄 MANUAL IP ROTATE", key="btn_rotate"):
        proxies = load_proxies(proxy_text)
        if proxies:
            st.session_state.proxy_index = (st.session_state.proxy_index + 1) % len(proxies)
            st.session_state.engine = RequestEngine(use_proxy_rotation=True, proxies=proxies)
            st.session_state.engine.proxy_index = st.session_state.proxy_index
            st.success(f"IP Rotated to: {proxies[st.session_state.proxy_index]}")
        else:
            st.error("No proxies in list!")

    st.markdown("---")
    start_btn = st.button("🚀 EXECUTE SCAN", key="btn_start")
    stop_btn = st.button("🛑 ABORT SCAN", key="btn_stop")


# Main Logic
if start_btn:
    if not target_input or not selected_modules:
        st.error("Target and Modules are required.")
    else:
        try:
            target = normalize_target(target_input)
            proxies = load_proxies(proxy_text)
            
            st.session_state.engine = RequestEngine(
                use_proxy_rotation=use_proxy, 
                proxies=proxies
            )
            
            st.info(f"[*] Engaging target: {target}")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            log_container = st.container()
            
            results = []
            is_blocked = False
            
            for i, module_name in enumerate(selected_modules):
                if is_blocked: break
                
                status_text.markdown(f"`[ RUNNING ]` -> **{module_name}**...")
                func = AVAILABLE_MODULES[module_name]
                
                try:
                    res = func(target, st.session_state.engine)
                    results.append(res)
                    
                    with log_container:
                        if res['findings']:
                            for finding in res['findings']:
                                sev = finding['severity']
                                det = finding['detail']
                                
                                # اگر شدت باگ بالا بود، با رنگ قرمز نشون بده
                                if sev in ["High", "Critical"]:
                                    st.error(f"[{sev}] {module_name.upper()} -> آسیب‌پذیری پیدا شد!")
                                    # متن‌های طولانی رو داخل منوی بازشونده بذار تا صفحه شلوغ نشه
                                    with st.expander("مشاهده جزئیات (URL, Payload, Response)"):
                                        st.code(det, language="bash")
                                else:
                                    with st.expander(f"[{sev}] {module_name.upper()} - اطلاعات"):
                                        st.code(det, language="bash")
                        else:
                            st.code(f"[-] {module_name.upper()} -> Clean / No findings.", language="bash")
                                
                except BlockDetected as e:
                    with log_container:
                        st.error(f"🛑 [WAF BLOCK DETECTED] {str(e)}")
                        st.error("⚠️ SCAN HALTED. Change your IP or wait before retrying.")
                    is_blocked = True
                    break 
                except Exception as e:
                    with log_container:
                        st.warning(f"[!] Error in {module_name}: {str(e)}")
                
                progress_bar.progress((i + 1) / len(selected_modules))
                
            if not is_blocked:
                status_text.markdown("`[ SCAN COMPLETE ]`")
                st.success("Scan finished successfully.")
                
                # HTML Report Generation
                if results:
                    html_content = f"""
                    <html>
                    <head><title>AutoHunter Report</title>
                    <style>
                        body {{ background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; padding: 20px; }}
                        table {{ border-collapse: collapse; width: 100%; border: 1px solid #00ff41; }}
                        th, td {{ border: 1px solid #333; padding: 10px; text-align: left; }}
                        th {{ background-color: #111; color: #ff003c; }}
                        .High {{ color: #ff003c; font-weight: bold; }}
                        .Info {{ color: #00aaff; }}
                    </style>
                    </head>
                    <body>
                        <h1>💀 AutoHunter Offensive Report</h1>
                        <p><b>Target:</b> {target}</p>
                        <p><b>Timestamp:</b> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                        <table>
                            <tr><th>Module</th><th>Status</th><th>Findings / Action Required</th></tr>
                    """
                    for res in results:
                        findings_html = "<br>".join([f"<span class='{f['severity']}'>[{f['severity']}]</span> {f['detail']}" for f in res['findings']]) if res['findings'] else "No direct findings"
                        html_content += f"<tr><td>{res['module']}</td><td>{res['status']}</td><td>{findings_html}</td></tr>"
                    html_content += """
                        </table>
                        <p style="margin-top: 40px; font-size: 12px; color: gray;">Generated by AutoHunter. Authorized testing only.</p>
                    </body></html>
                    """
                    st.download_button(
                        label="⬇️ DOWNLOAD HTML REPORT",
                        data=html_content,
                        file_name=f"autohunter_report_{int(time.time())}.html",
                        mime="text/html",
                        key="btn_download"
                    )
        except Exception as e:
            st.error(f"Fatal Error: {e}")

if stop_btn:
    st.warning("Abort signal sent. Terminating current UI loop.")
