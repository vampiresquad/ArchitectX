#!/usr/bin/env python3
# ======================================================================
# [ ©ArchitectX 2.0 Enterprise - Developed by Muhammad Shourov ]
# [ ALL RIGHTS RESERVED | VAMPIRE SQUAD                        ]
# ======================================================================

import json
import requests
import time
import re
import http.client
from rich.console import Console

console = Console()

# [ এথিক্যাল ফিল্টার ]
BLOCKED_KEYWORDS = ["ddos", "ransomware", "phishing", "malware", "virus", "exploit", "hack bank", "steal password", "trojan", "carding"]

def verify_ethics(prompt):
    prompt_lower = prompt.lower()
    for word in BLOCKED_KEYWORDS:
        if re.search(rf"\b{word}\b", prompt_lower):
            return False, word
    return True, None

def fetch_web_context(query, api_key, spinner):
    """Serper API ব্যবহার করে ইন্টারনেট থেকে লেটেস্ট লাইব্রেরি বা ডিজাইন সার্চ করা"""
    spinner.update(f"Scanning the web via Serper nodes for: {query[:20]}...", style="cyan")
    try:
        conn = http.client.HTTPSConnection("google.serper.dev", timeout=12)
        payload = json.dumps({"q": query})
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read()
        
        result_json = json.loads(data.decode("utf-8"))
        extracted_info = ""
        if "organic" in result_json:
            for item in result_json["organic"][:3]:
                extracted_info += f"- {item.get('title')}: {item.get('snippet')}\n"
        return extracted_info
    except:
        return "Offline Mode: Web context unavailable."

def generate_offline_template(project_type, user_prompt):
    """API না থাকলে বা ফেইল করলে লোকাল টেমপ্লেট দেবে"""
    if project_type in ["webapp", "website"]:
        html = f"""<!DOCTYPE html>
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
            <p>Generated via ArchitectX Offline Core. Context: {user_prompt[:50]}...</p>
        </header>
        <main id="app-content">
            <div class="card">
                <h2>Module Active</h2>
                <p>System is running on local fallback templates due to AI timeout.</p>
                <button id="actionBtn">Initialize</button>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""
        css = ":root { --bg: #0d1117; --text: #c9d1d9; --accent: #00ff00; }\nbody { background: var(--bg); color: var(--text); font-family: monospace; padding: 20px; }\n.card { border: 1px solid #30363d; padding: 20px; border-radius: 8px; }\nbutton { background: transparent; border: 1px solid var(--accent); color: var(--accent); padding: 10px; cursor: pointer; }"
        js = "console.log('ArchitectX Offline UI Loaded.');"
        return {"index.html": html, "style.css": css, "script.js": js}
    else:
        py_code = f"#!/usr/bin/env python3\n# Prompt: {user_prompt[:40]}\nprint('[*] ArchitectX Offline Tool Initialized.')\n"
        return {"main.py": py_code}

def generate_code(project_type, user_prompt, active_apis, spinner_engine):
    """Z.ai এবং Serper দিয়ে ফাইনাল কোড জেনারেশন (The Master Router)"""
    
    is_ethical, bad_word = verify_ethics(user_prompt)
    if not is_ethical:
        spinner_engine.stop(f"SECURITY ALERT: Unethical request blocked ('{bad_word}').", success=False)
        return None

    # ১. ওয়েব কনটেক্সট (যদি Serper থাকে)
    web_context = ""
    if active_apis.get("serper_key"):
        web_context = fetch_web_context(f"Modern UI design structure for {project_type} {user_prompt[:20]}", active_apis["serper_key"], spinner_engine)

    # ২. প্রম্পট ইঞ্জিনিয়ারিং
    system_instruction = f"""
    You are ArchitectX 2.0, an elite code generator created by Muhammad Shourov (Vampire Squad).
    Project: {project_type}
    Requirements: {user_prompt}
    Web Context: {web_context}
    
    CRITICAL RULES:
    1. Output MUST be ONLY a valid JSON object. No explanations, no markdown tags.
    2. Keys are exact filenames ('index.html', 'style.css', 'main.py').
    3. Values must be the FULL, COMPLETE code. Do not use placeholders.
    4. For Web: Ensure highly professional UI/UX. For Python: Ensure error handling.
    """

    # ৩. Z.ai (Zhipu AI) রিকোয়েস্ট
    if active_apis.get("zai_key"):
        spinner_engine.update("Compiling prompt & Routing to Z.ai Neural Core...", style="magenta")
        try:
            url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
            headers = {"Authorization": f"Bearer {active_apis['zai_key']}", "Content-Type": "application/json"}
            data = {
                "model": "glm-4",
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": "Generate the JSON response now."}
                ],
                "temperature": 0.2
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=90)
            response.raise_for_status()
            
            result = response.json()
            generated_text = result['choices'][0]['message']['content']
            
            # JSON ফরম্যাট ফিক্স করা
            generated_text = generated_text.replace("```json", "").replace("```", "").strip()
            code_dict = json.loads(generated_text)
            
            spinner_engine.stop("AI Code matrix compiled perfectly!")
            return code_dict
            
        except Exception as e:
            spinner_engine.update(f"AI Generation Error: {e}. Switching to Offline Core...", style="red")
            time.sleep(1)

    # ৪. ফলব্যাক: অফলাইন জেনারেটর
    spinner_engine.stop("Falling back to ArchitectX Offline Engine.", success=False)
    return generate_offline_template(project_type, user_prompt)
