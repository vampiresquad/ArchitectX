#!/usr/bin/env python3
# ======================================================================
# [ ©ArchitectX 2.0 Enterprise - Developed by Muhammad Shourov ]
# [ ALL RIGHTS RESERVED | VAMPIRE SQUAD                        ]
# ======================================================================

import base64
import json
import http.client
import requests
from rich.console import Console
from core.config_loader import load_config

console = Console()

# ভল্ট: ইন-বিল্ট এপিআই (Base64 Encoded for protection)
ENCODED_SERPER_KEYS = [
    "ZTI1YzEyYjk0NzAwYjEyN2NiMjRlNDlmYzU0ODJiMmRiMTY1N2Q0Yw==",
    "NzkyMzQ2YjczY2M5ZTIxMTdjNTYwMmMxNjUyZjE5OTUwMzM3NDk1MQ=="
]
ENCODED_ZAI_KEY = "Mjg2NTlmNjEzYTM4NDUxMGIzMTIwYWNiMzYwYjEwZGUuOGJXbzBBZnU2WXQ3eFBPTA=="

def get_vault_key(service, index=0):
    """ডিকোড করে ইন-বিল্ট কি (Key) প্রোভাইড করে"""
    try:
        if service == "zai":
            return base64.b64decode(ENCODED_ZAI_KEY).decode('utf-8')
        elif service == "serper":
            return base64.b64decode(ENCODED_SERPER_KEYS[index % len(ENCODED_SERPER_KEYS)]).decode('utf-8')
    except Exception:
        return None

class APIRouter:
    """এপিআই ম্যানেজমেন্ট এবং হেলথ চেকিং ইঞ্জিন"""
    def __init__(self):
        self.active_zai = None
        self.active_serper = None
        self.config = load_config()

    def check_zai_health(self, api_key):
        """Zhipu AI সার্ভার জ্যান্ত আছে কি না চেক করে"""
        try:
            url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            data = {"model": "glm-4", "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
            response = requests.post(url, headers=headers, json=data, timeout=8)
            return response.status_code == 200
        except:
            return False

    def check_serper_health(self, api_key):
        """Serper.dev সার্চ ইঞ্জিন চেক করে"""
        try:
            conn = http.client.HTTPSConnection("google.serper.dev", timeout=8)
            payload = json.dumps({"q": "ArchitectX ping"})
            headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
            conn.request("POST", "/search", payload, headers)
            res = conn.getresponse()
            return res.status == 200
        except:
            return False

    def initialize_engines(self, spinner_engine):
        """সবচেয়ে বেস্ট এবং রানিং এপিআই সিলেক্ট করে"""
        spinner_engine.update("Routing Z.ai Neural Network...", "magenta")
        
        user_zai = self.config.get("user_zai_key")
        if user_zai and self.check_zai_health(user_zai):
            self.active_zai = user_zai
        else:
            builtin_zai = get_vault_key("zai")
            if builtin_zai and self.check_zai_health(builtin_zai):
                self.active_zai = builtin_zai

        spinner_engine.update("Scanning Serper.dev global nodes...", "cyan")
        
        user_serper = self.config.get("user_serper_key")
        if user_serper and self.check_serper_health(user_serper):
            self.active_serper = user_serper
        else:
            builtin_serper = get_vault_key("serper", 0)
            if builtin_serper and self.check_serper_health(builtin_serper):
                self.active_serper = builtin_serper
                
        # স্ট্যাটাস রিপোর্ট রিটার্ন করে (ড্যাশবোর্ডের জন্য)
        zai_status = "Online (User)" if user_zai == self.active_zai else ("Online (Built-in)" if self.active_zai else "Offline")
        serper_status = "Online (User)" if user_serper == self.active_serper else ("Online (Built-in)" if self.active_serper else "Offline")
        
        return {
            "zai_key": self.active_zai,
            "serper_key": self.active_serper,
            "zai_status": zai_status,
            "serper_status": serper_status
        }
