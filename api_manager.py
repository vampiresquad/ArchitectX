import base64
import json
import http.client
import requests
import time
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

console = Console()

# =====================================================================
# ArchitectX Core: API Obfuscation (In-built Keys)
# আপনার দেওয়া API Key গুলোকে Base64 দিয়ে এনকোড করে রাখা হলো 
# যাতে সোর্স কোডে সরাসরি দেখা না যায়।
# =====================================================================
ENCODED_SERPER_KEYS = [
    "ZTI1YzEyYjk0NzAwYjEyN2NiMjRlNDlmYzU0ODJiMmRiMTY1N2Q0Yw==",
    "NzkyMzQ2YjczY2M5ZTIxMTdjNTYwMmMxNjUyZjE5OTUwMzM3NDk1MQ=="
]
ENCODED_ZAI_KEY = "Mjg2NTlmNjEzYTM4NDUxMGIzMTIwYWNiMzYwYjEwZGUuOGJXbzBBZnU2WXQ3eFBPTA=="

def get_builtin_key(service):
    """এনকোড করা কি (Key) গুলো ডিকোড করে রিটার্ন করবে।"""
    try:
        if service == "zai":
            return base64.b64decode(ENCODED_ZAI_KEY).decode('utf-8')
        elif service == "serper":
            # আপাতত প্রথম কি-টি রিটার্ন করছি, চাইলে রাউন্ড-রবিন লজিক করা যায়
            return base64.b64decode(ENCODED_SERPER_KEYS[0]).decode('utf-8')
    except Exception as e:
        return None

# =====================================================================
# ArchitectX Core: UX Engine (Live Status & Spinners)
# ব্যাকগ্রাউন্ড টাস্ক চলার সময় ইউজারের জন্য চমৎকার লাইভ আপডেট।
# =====================================================================
class ArchitectXSpinner:
    def __init__(self, initial_text="Initializing ArchitectX Core..."):
        self.spinner = Spinner("dots", text=Text(initial_text, style="cyan"))
        self.live = Live(self.spinner, refresh_per_second=15, transient=True)
        
    def start(self):
        self.live.start()
        
    def update(self, text, style="yellow"):
        self.spinner.text = Text(text, style=style)
        
    def stop(self):
        self.live.stop()

# =====================================================================
# ArchitectX Core: API Health Check & Router
# =====================================================================
def check_serper_health(api_key):
    """Serper.dev API ঠিকঠাক কাজ করছে কি না তা চেক করে।"""
    try:
        conn = http.client.HTTPSConnection("google.serper.dev", timeout=10)
        payload = json.dumps({"q": "test"})
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read()
        
        if res.status == 200:
            return True
        return False
    except Exception as e:
        return False

def check_zai_health(api_key):
    """Zhipu AI (Z.ai) API জ্যান্ত আছে কি না তা চেক করে।"""
    try:
        # Zhipu AI এর মডেল লিস্ট বা ডামি চ্যাট রিকোয়েস্ট দিয়ে চেক
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "glm-4",
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 5
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        return False

def get_active_apis(user_zai_key=None, user_serper_key=None):
    """
    ইউজারের API এবং ইন-বিল্ট API চেক করে সবচেয়ে বেস্ট এবং অ্যাক্টিভ API রিটার্ন করে।
    """
    active_keys = {"zai": None, "serper": None}
    
    spinner = ArchitectXSpinner("Verifying API Health Connections...")
    spinner.start()
    
    # 1. Z.ai Health Check
    spinner.update("Pinging Z.ai Neural Network...", style="magenta")
    time.sleep(1) # UX এর জন্য হালকা ডিলে
    
    if user_zai_key and check_zai_health(user_zai_key):
        active_keys["zai"] = user_zai_key
    else:
        spinner.update("User Z.ai key missing/failed. Switching to ArchitectX Core API...", style="yellow")
        time.sleep(0.8)
        builtin_zai = get_builtin_key("zai")
        if check_zai_health(builtin_zai):
            active_keys["zai"] = builtin_zai
            
    # 2. Serper.dev Health Check
    spinner.update("Checking Serper.dev Web Search nodes...", style="cyan")
    time.sleep(1)
    
    if user_serper_key and check_serper_health(user_serper_key):
        active_keys["serper"] = user_serper_key
    else:
        spinner.update("Switching to ArchitectX Core Serper API...", style="yellow")
        time.sleep(0.8)
        builtin_serper = get_builtin_key("serper")
        if check_serper_health(builtin_serper):
            active_keys["serper"] = builtin_serper
            
    spinner.stop()
    
    # ফাইনাল রিপোর্ট
    if active_keys["zai"]:
        console.print("[bold green][✔] Z.ai Engine: ONLINE[/bold green]")
    else:
        console.print("[bold red][!] Z.ai Engine: OFFLINE (All keys failed)[/bold red]")
        
    if active_keys["serper"]:
        console.print("[bold green][✔] Serper.dev Search: ONLINE[/bold green]")
    else:
        console.print("[bold red][!] Serper.dev Search: OFFLINE[/bold red]")
        
    return active_keys

# =====================================================================
# ArchitectX Core: Web Search Extractor (Powered by Serper)
# =====================================================================
def search_web_for_context(query, api_key):
    """
    ইউজারের প্রজেক্টের জন্য লেটেস্ট তথ্য, CSS ফ্রেমওয়ার্ক বা ডিজাইন ট্রেন্ড 
    ইন্টারনেট থেকে সার্চ করে নিয়ে আসে।
    """
    spinner = ArchitectXSpinner(f"Scanning the web for: {query}...")
    spinner.start()
    
    try:
        conn = http.client.HTTPSConnection("google.serper.dev", timeout=15)
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read()
        
        result_json = json.loads(data.decode("utf-8"))
        
        # অর্গানিক সার্চ রেজাল্ট থেকে টাইটেল এবং স্নাইপেট আলাদা করা
        extracted_info = ""
        if "organic" in result_json:
            for item in result_json["organic"][:3]: # প্রথম ৩টি রেজাল্ট
                extracted_info += f"- {item.get('title')}: {item.get('snippet')}\n"
                
        spinner.stop()
        console.print("[bold green][✔] Web data extracted successfully![/bold green]")
        return extracted_info
        
    except Exception as e:
        spinner.stop()
        console.print(f"[bold red][!] Web Search failed: {e}[/bold red]")
        return None

# টেস্ট করার জন্য ডামি রান
if __name__ == "__main__":
    console.print("\n[bold cyan]--- ArchitectX API Manager Diagnostics ---[/bold cyan]")
    keys = get_active_apis()
    if keys["serper"]:
        context = search_web_for_context("latest dark mode css UI design trends 2026", keys["serper"])
        print(f"\nExtracted Context:\n{context}")
