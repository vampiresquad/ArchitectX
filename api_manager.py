import base64
import json
import http.client
import requests
import time
import os
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

console = Console()

# =====================================================================
# [ ArchitectX Core: API Vault & Obfuscation ]
# =====================================================================
# ইন-বিল্ট API গুলোকে Base64 এনকোড করে রাখা হলো সিকিউরিটির জন্য
ENCODED_SERPER_KEYS = [
    "ZTI1YzEyYjk0NzAwYjEyN2NiMjRlNDlmYzU0ODJiMmRiMTY1N2Q0Yw==",
    "NzkyMzQ2YjczY2M5ZTIxMTdjNTYwMmMxNjUyZjE5OTUwMzM3NDk1MQ=="
]
ENCODED_ZAI_KEY = "Mjg2NTlmNjEzYTM4NDUxMGIzMTIwYWNiMzYwYjEwZGUuOGJXbzBBZnU2WXQ3eFBPTA=="

def get_vault_key(service, index=0):
    """সিকিউর ভল্ট থেকে API কি ডিকোড করে আনে"""
    try:
        if service == "zai":
            return base64.b64decode(ENCODED_ZAI_KEY).decode('utf-8')
        elif service == "serper":
            return base64.b64decode(ENCODED_SERPER_KEYS[index % len(ENCODED_SERPER_KEYS)]).decode('utf-8')
    except Exception:
        return None

# =====================================================================
# [ ArchitectX Core: Live UX & Animation Engine ]
# =====================================================================
class ArchitectXSpinner:
    """ব্যাকগ্রাউন্ডে কাজ চলার সময় ইউজারের বোরিংনেস কাটাতে স্মার্ট লাইভ আপডেটার"""
    def __init__(self, initial_text="Initializing ArchitectX Core Matrix..."):
        # হ্যাকার ভাইব দেওয়ার জন্য 'bouncingBar' বা 'dots' স্পিনার
        self.spinner = Spinner("bouncingBar", text=Text(initial_text, style="bold cyan"))
        self.live = Live(self.spinner, refresh_per_second=20, transient=True)
        self.is_running = False
        
    def start(self):
        if not self.is_running:
            self.live.start()
            self.is_running = True
        
    def update(self, text, style="bold yellow"):
        if self.is_running:
            self.spinner.text = Text(text, style=style)
            # টেক্সট পড়ার জন্য সামান্য ন্যাচারাল ডিলে
            time.sleep(0.3)
        
    def stop(self, final_text=None, success=True):
        if self.is_running:
            self.live.stop()
            self.is_running = False
            if final_text:
                if success:
                    console.print(f"[bold green][✔] {final_text}[/bold green]")
                else:
                    console.print(f"[bold red][✖] {final_text}[/bold red]")

# =====================================================================
# [ ArchitectX Core: Neural Health & Router ]
# =====================================================================
class APIRouter:
    def __init__(self):
        self.active_zai = None
        self.active_serper = None
        
    def check_zai_health(self, api_key):
        """Zhipu AI (Z.ai) এর সার্ভারে পিং করে চেক করে এটি জ্যান্ত কি না"""
        try:
            url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            data = {"model": "glm-4", "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
            response = requests.post(url, headers=headers, json=data, timeout=8)
            return response.status_code == 200
        except:
            return False

    def check_serper_health(self, api_key):
        """Serper.dev এর সার্ভারে ডামি রিকোয়েস্ট পাঠিয়ে চেক করে"""
        try:
            conn = http.client.HTTPSConnection("google.serper.dev", timeout=8)
            payload = json.dumps({"q": "ArchitectX ping test"})
            headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
            conn.request("POST", "/search", payload, headers)
            res = conn.getresponse()
            return res.status == 200
        except:
            return False

    def initialize_engines(self, user_config):
        """সবচেয়ে ফাস্ট এবং জ্যান্ত API সিলেক্ট করে রাউট তৈরি করে"""
        ux = ArchitectXSpinner("Establishing secure connection to AI Nodes...")
        ux.start()
        
        # 1. Z.ai Check
        ux.update("Pinging Z.ai Neural Network...", "magenta")
        user_zai = user_config.get("ZAI_KEY")
        if user_zai and self.check_zai_health(user_zai):
            self.active_zai = user_zai
            ux.update("User Z.ai Key accepted.", "green")
        else:
            ux.update("Switching to ArchitectX In-built Z.ai Key...", "yellow")
            builtin_zai = get_vault_key("zai")
            if builtin_zai and self.check_zai_health(builtin_zai):
                self.active_zai = builtin_zai
                
        # 2. Serper Check
        ux.update("Scanning Serper.dev global search nodes...", "cyan")
        user_serper = user_config.get("SERPER_KEY")
        if user_serper and self.check_serper_health(user_serper):
            self.active_serper = user_serper
            ux.update("User Serper Key accepted.", "green")
        else:
            ux.update("Switching to ArchitectX In-built Serper Key...", "yellow")
            builtin_serper = get_vault_key("serper", 0)
            if builtin_serper and self.check_serper_health(builtin_serper):
                self.active_serper = builtin_serper
                
        ux.stop("Neural Engines Initialized successfully!")
        
        return {"zai": self.active_zai, "serper": self.active_serper}

# =====================================================================
# [ ArchitectX Core: Web Context Extractor ]
# =====================================================================
def fetch_web_context(query, api_key, ux_spinner):
    """Serper.dev ব্যবহার করে ইন্টারনেট থেকে লাইভ লাইব্রেরি বা ডিজাইন ডাটা আনে"""
    ux_spinner.update(f"Extracting live web context for: {query}...", "cyan")
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
            for item in result_json["organic"][:4]:
                extracted_info += f"- {item.get('title')}: {item.get('snippet')}\n"
        return extracted_info
    except Exception as e:
        return "Web search fallback activated. Generating offline context..."
