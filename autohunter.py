import streamlit as st
import time
import datetime
from autohunter_core import normalize_target, load_proxies, RequestEngine, BlockDetected
from wrappers import AVAILABLE_MODULES

# Page Configuration
st.set_page_config(page_title="AutoHunter", page_icon="🕵️", layout="wide")

st.title("🕵️ AutoHunter")
st.markdown("**Automated Recon & Vulnerability Scanner**")
st.markdown("---")

# Sidebar for Settings
with st.sidebar:
    st.header("⚙️ Settings")
    target_input = st.text_input("Target (Domain or URL)", "http://127.0.0.1:8001")
    
    st.subheader("Modules")
    selected_modules = st.multiselect(
        "Select modules to run:",
        options=list(AVAILABLE_MODULES.keys()),
        default=list(AVAILABLE_MODULES.keys())
    )
    
    st.subheader("Advanced")
    use_proxy = st.checkbox("Use Proxy Rotation")
    proxy_text = st.text_area("Proxy List (one per line)", placeholder="http://ip:port\nsocks5://ip:port")
    
    start_btn = st.button("🚀 Start Scan", use_container_width=True)

# Main Area
if start_btn:
    if not target_input:
        st.error("Please enter a target.")
    elif not selected_modules:
        st.error("Please select at least one module.")
    else:
        try:
            # Normalize target and setup engine
            target = normalize_target(target_input)
            proxies = load_proxies(proxy_text) if use_proxy else []
            engine = RequestEngine(use_proxy_rotation=use_proxy, proxies=proxies)
            
            st.info(f"Starting scan on: **{target}**")
            
            # UI Elements for live updates
            progress_bar = st.progress(0)
            status_text = st.empty()
            log_area = st.container()
            
            results = []
            
            for i, module_name in enumerate(selected_modules):
                status_text.text(f"Running module: {module_name}...")
                func = AVAILABLE_MODULES[module_name]
                
                try:
                    # Run the module
                    res = func(target, engine)
                    results.append(res)
                    
                    # Display result in live log
                    with log_area:
                        st.success(f"✅ **{module_name}** finished with status: `{res['status']}`")
                        if res['findings']:
                            for finding in res['findings']:
                                st.write(f" - `[{finding['severity']}]` {finding['detail']}")
                                
                except BlockDetected as e:
                    with log_area:
                        st.error(f"🛑 **Blocked** while running {module_name}. Stopping scan.")
                    break # Stop if blocked
                except Exception as e:
                    with log_area:
                        st.error(f"❌ **Error** in {module_name}: {str(e)}")
                
                # Update progress
                progress_bar.progress((i + 1) / len(selected_modules))
                time.sleep(0.5) # Small delay for UI smoothness
                
            status_text.text("Scan Complete!")
            st.balloons()
            
            # --- Generate HTML Report ---
            if results:
                st.markdown("### 📄 Download Report")
                
                # HTML Generation Logic
                html_content = f"""
                <html>
                <head>
                    <title>AutoHunter Report</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; padding: 20px; }}
                        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                        th {{ background-color: #f2f2f2; }}
                        .Critical {{ color: red; font-weight: bold; }}
                        .High {{ color: orange; font-weight: bold; }}
                        .Medium {{ color: #d4a017; }}
                        .Low {{ color: blue; }}
                        .Info {{ color: gray; }}
                    </style>
                </head>
                <body>
                    <h1>AutoHunter Scan Report</h1>
                    <p><b>Target:</b> {target}</p>
                    <p><b>Date:</b> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                    <table>
                        <tr><th>Module</th><th>Status</th><th>Findings</th></tr>
                """
                
                for res in results:
                    findings_html = ""
                    if res['findings']:
                        findings_html = "<br>".join([f"<span class='{f['severity']}'>[{f['severity']}]</span> {f['detail']}" for f in res['findings']])
                    else:
                        findings_html = "No findings"
                        
                    html_content += f"<tr><td>{res['module']}</td><td>{res['status']}</td><td>{findings_html}</td></tr>"
                    
                html_content += """
                    </table>
                    <p style="margin-top: 40px; font-size: 12px; color: gray;">
                        <i>Disclaimer: This tool is for authorized testing only. The developer is not responsible for any misuse.</i>
                    </p>
                </body>
                </html>
                """
                
                st.download_button(
                    label="⬇️ Download HTML Report",
                    data=html_content,
                    file_name=f"autohunter_report_{int(time.time())}.html",
                    mime="text/html"
                )
                
        except Exception as e:
            st.error(f"Fatal Error: {e}")
