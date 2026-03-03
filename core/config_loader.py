#!/usr/bin/env python3
# ======================================================================
# [ ©ArchitectX 2.0 Enterprise - Developed by Muhammad Shourov ]
# [ ALL RIGHTS RESERVED | VAMPIRE SQUAD                        ]
# ======================================================================

import os
import json
from rich.console import Console

console = Console()
CONFIG_FILE = os.path.expanduser("~/.architectx_vault.json")

def load_config():
    """ইউজারের কনফিগারেশন এবং এপিআই কিংস (Keys) লোড করবে।
       ফাইল না থাকলে একটি ডিফল্ট টেমপ্লেট তৈরি করে দেবে।"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass # ফাইল করাপ্টেড হলে ডিফল্ট রিটার্ন করবে
            
    # ডিফল্ট কনফিগারেশন স্ট্রাকচার
    default_config = {
        "user_zai_key": None,
        "user_serper_key": None,
        "preferred_hosting": "localhost",
        "auto_heal_code": True
    }
    save_config(default_config)
    return default_config

def save_config(config_data):
    """যেকোনো নতুন সেটিংস বা আপডেট হওয়া কি (Key) সেভ করবে।"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)
        return True
    except Exception as e:
        console.print(f"[bold red][!] Vault Error: Failed to save configuration. {e}[/bold red]")
        return False

def update_key(key_name, key_value):
    """নির্দিষ্ট কোনো কি (Key) আপডেট করার ডাইনামিক ফাংশন।"""
    config = load_config()
    config[key_name] = key_value
    save_config(config)
