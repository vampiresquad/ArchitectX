import json
import requests
import time
import re
from rich.console import Console
from api_manager import ArchitectXSpinner, fetch_web_context

console = Console()

# =====================================================================
# [ ArchitectX Core: Ethical Firewall ]
# =====================================================================
BLOCKED_KEYWORDS = [
    "ddos", "ransomware", "phishing", "malware", "virus", 
    "exploit", "hack bank", "steal password", "trojan", "keylogger",
    "carding", "bypass otp", "sql injection payload"
]

def verify_ethics(prompt):
    """কড়া এথিক্যাল চেক: অবৈধ রিকোয়েস্ট প্রথমেই আটকে দেবে"""
    prompt_lower = prompt.lower()
    for word in BLOCKED_KEYWORDS:
        if re.search(rf"\b{word}\b", prompt_lower):
            return False, word
    return True, None

# =====================================================================
# [ ArchitectX Core: Offline Dynamic Template Engine (No-API Fallback) ]
# =====================================================================
def generate_offline_template(project_type, user_prompt):
    """
    যদি কোনো API কাজ না করে, ArchitectX তার নিজস্ব লজিক ব্যবহার করে 
    লেগো (Lego) ব্লকের মতো কোড সাজিয়ে আউটপুট দেবে।
    """
    console.print("\n[bold yellow][!] Warning: All AI Nodes unreachable. Activating Offline Template Engine...[/bold yellow]")
    time.sleep(1)
    
    # বেসিক প্রোডাকশন-রেডি টেমপ্লেট
    if project_type in ["webapp", "website"]:
        html_code = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ArchitectX Auto-Generated {project_type.title()}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body class="dark-theme">
    <div class="container">
        <header>
            <h1>{project_type.upper()} WORKSPACE</h1>
            <p>Generated via ArchitectX Offline Core. Prompt context: {user_prompt[:50]}...</p>
        </header>
        <main id="app-content">
            <div class="card">
                <h2>Module 1</h2>
                <p>System is running on local fallback templates. Connect API for AI dynamic generation.</p>
                <button id="actionBtn">Initialize</button>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""
        css_code = """
:root { --bg-color: #0d1117; --text-color: #c9d1d9; --accent: #00ff00; }
body { margin: 0; padding: 0; background-color: var(--bg-color); color: var(--text-color); font-family: 'Courier New', Courier, monospace; }
.container { max-width: 1000px; margin: 0 auto; padding: 20px; }
header { border-bottom: 1px solid #30363d; padding-bottom: 20px; margin-bottom: 20px; }
h1, h2 { color: var(--accent); }
.card { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 8px; }
button { background: transparent; border: 1px solid var(--accent); color: var(--accent); padding: 10px 20px; cursor: pointer; font-family: inherit; transition: 0.3s; }
button:hover { background: var(--accent); color: #000; }
"""
        js_code = """
document.addEventListener('DOMContentLoaded', () => {
    console.log("ArchitectX Offline Core Initialized.");
    const btn = document.getElementById('actionBtn');
    if(btn) {
        btn.addEventListener('click', () => alert('ArchitectX Offline Action Triggered!'));
    }
});
"""
        return {"index.html": html_code, "style.css": css_code, "script.js": js_code}
        
    elif project_type == "tools":
        py_code = f"""#!/usr/bin/env python3
# ArchitectX Offline Auto-Generated Tool
import sys
import time

def main():
    print("\\n[*] Initializing Tool generated from prompt: {user_prompt[:30]}...")
    time.sleep(1)
    print("[+] Core modules loaded.")
    print("[-] Note: This is an offline template. AI generation was offline.")
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
"""
        return {"main.py": py_code}
    
    return {}

# =====================================================================
# [ ArchitectX Core: Multi-Agent Neural Router ]
# =====================================================================
def generate_code(project_type, user_prompt, active_apis, ux_spinner):
    """
    Z.ai এবং Serper (বা Gemini) ব্যবহার করে প্রোডাকশন-রেডি কোড তৈরি করে।
    """
    is_ethical, bad_word = verify_ethics(user_prompt)
    if not is_ethical:
        ux_spinner.stop(f"SECURITY ALERT: Unethical request blocked (Keyword: '{bad_word}').", success=False)
        return None

    # ১. ওয়েব থেকে লাইভ কনটেক্সট আনা (যদি Serper একটিভ থাকে)
    web_context = ""
    if active_apis.get("serper"):
        web_context = fetch_web_context(f"best UI design code structure for {project_type} {user_prompt[:30]}", active_apis["serper"], ux_spinner)
    
    # ২. প্রম্পট ইঞ্জিনিয়ারিং
    system_instruction = f"""
    You are ArchitectX, an elite, professional code generator developed by Muhammad Shourov (Vampire Squad).
    Project Type: {project_type}
    User Requirements: {user_prompt}
    Live Web Context: {web_context}
    
    CRITICAL RULES:
    1. Output MUST be ONLY a valid JSON object. No markdown tags, no explanations.
    2. Keys must be filenames (e.g., 'index.html', 'style.css', 'script.js', 'main.py').
    3. Values must be complete, production-ready code.
    4. For tools, ensure robust error handling. For web, ensure modern, responsive UI.
    """

    # ৩. Z.ai (Zhipu AI) এর মাধ্যমে জেনারেশন
    if active_apis.get("zai"):
        ux_spinner.update("Routing prompt to Z.ai Neural Core...", "magenta")
        try:
            url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
            headers = {
                "Authorization": f"Bearer {active_apis['zai']}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "glm-4",
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": "Generate the project in JSON format."}
                ],
                "temperature": 0.2
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            generated_text = result['choices'][0]['message']['content']
            
            # JSON ফরম্যাটিং ফিক্সিং (যদি AI ভুল করে markdown দেয়)
            generated_text = generated_text.replace("```json", "").replace("```", "").strip()
            
            code_dict = json.loads(generated_text)
            ux_spinner.stop("Z.ai Code matrix compiled successfully!")
            return code_dict
            
        except Exception as e:
            ux_spinner.update(f"Z.ai Generation failed: {e}. Attempting offline recovery...", "red")
            time.sleep(1)
            
    # ৪. ফলব্যাক: অফলাইন জেনারেটর
    ux_spinner.stop("Falling back to Offline Core.", success=False)
    return generate_offline_template(project_type, user_prompt)
