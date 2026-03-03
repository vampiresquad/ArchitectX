#!/usr/bin/env python3
# ======================================================================
# [ ©ArchitectX 2.0 Enterprise - Developed by Muhammad Shourov ]
# [ ALL RIGHTS RESERVED | VAMPIRE SQUAD                        ]
# ======================================================================

import os
import platform
import subprocess
import hashlib
import uuid
import requests
import sys
import time
import shutil
import re
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

# --- কনফিগারেশন এবং সেটআপ ---
console = Console()
APPROVED_LIST_URL = "https://raw.githubusercontent.com/vampiresquad/Paid_Approval/refs/heads/main/approved.txt"
DEVICE_FILE = os.path.expanduser("~/.vs_hwid_config") # হিডেন ব্যাকআপ ফাইল

# ANSI কালার কোড (আপনার তৈরি করা অরিজিনাল কালারগুলো)
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

# --- ইউটিলিটি ফাংশন (আপনার অরিজিনাল অ্যানিমেশন লজিক) ---

def get_terminal_width():
    try: return shutil.get_terminal_size().columns
    except: return 80

def _strip_ansi(s: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*m", "", s)

def center_text(text):
    width = get_terminal_width()
    text_length = len(_strip_ansi(text))
    return ' ' * ((width - text_length) // 2) + text

def slow_print(text, delay=0.02, center=False):
    if center: text = center_text(text)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# --- ফিক্সড ডিভাইস আইডি লজিক ---

def get_permanent_id():
    """ডিভাইসের হার্ডওয়্যার ভিত্তিক স্থায়ী আইডি জেনারেট করে"""
    
    if os.path.exists(DEVICE_FILE):
        with open(DEVICE_FILE, "r") as f:
            saved_id = f.read().strip()
            if saved_id: return saved_id

    hw_string = ""
    system = platform.system()
    
    try:
        if "ANDROID_ROOT" in os.environ or "PREFIX" in os.environ:
            hw_string = subprocess.check_output("settings get secure android_id", shell=True).decode().strip()
        elif system == "Windows":
            hw_string = subprocess.check_output("wmic csproduct get uuid", shell=True).decode().split('\n')[1].strip()
        else:
            hw_string = str(uuid.getnode())
    except:
        hw_string = str(uuid.getnode())

    final_id = "VS-" + hashlib.sha256(hw_string.encode()).hexdigest()[:16].upper()
    
    try:
        with open(DEVICE_FILE, "w") as f:
            f.write(final_id)
    except: pass
    
    return final_id

# --- ইন্টারফেস এবং ভেরিফিকেশন ---

def draw_denied_box(device_id):
    """অ্যাক্সেস ডিনাইড হলে প্রফেশনাল বক্স দেখাবে"""
    console.clear()
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    denied_text = Text()
    denied_text.append(f"\nDEVICE ID: {device_id}\n", style="bold cyan")
    denied_text.append("STATUS: UNAUTHORIZED\n", style="bold red blink")
    denied_text.append("\nContact Muhammad Shourov for premium approval.\n", style="yellow")
    denied_text.append("Send the Device ID shown above to the admin.\n\n", style="bold white")
    denied_text.append(f"Timestamp: {current_time}\n", style="dim white")
    denied_text.append("Security Protocol: VAMPIRE SQUAD CORE", style="bold magenta")
    
    box_panel = Panel.fit(
        denied_text, 
        title="[bold red]✖ SYSTEM LOCKDOWN ✖[/bold red]", 
        border_style="red", 
        padding=(1, 3)
    )
    console.print(Align.center(box_panel))
    
    slow_print(f"\n{MAGENTA}Press Enter to exit system...{RESET}", center=True)
    input()
    sys.exit(1)

def verify_license(spinner_engine=None):
    """পেইড লাইসেন্স চেকার এবং ভেরিফিকেশন ইঞ্জিন (ArchitectX 2.0 Integrated)"""
    
    # মেইন লঞ্চার থেকে আসলে স্পিনার থামিয়ে আমাদের কাস্টম অ্যানিমেশন শুরু করবে
    if spinner_engine:
        spinner_engine.stop("Initializing Vampire Squad Security Core...")
        
    console.clear()
    slow_print(center_text(f"{BOLD}{CYAN}VAMPIRE SQUAD PREMIUM ACCESS SYSTEM{RESET}"), 0.04)
    slow_print(center_text(f"{CYAN}{'='*50}{RESET}"), 0.01)
    
    device_id = get_permanent_id()
    
    try:
        with console.status("[bold yellow]Authenticating with Global Servers...", spinner="aesthetic"):
            response = requests.get(APPROVED_LIST_URL, timeout=15)
            if response.status_code == 200:
                approved_list = [line.strip() for line in response.text.splitlines() if line.strip()]
            else:
                approved_list = []
    except Exception:
        slow_print(f"\n{RED}[!] Network Error: Shield activated. check your connection.{RESET}", center=True)
        sys.exit(1)

    if device_id in approved_list:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        success_msg = (
            f"[bold green]AUTHENTICATION SUCCESSFUL[/bold green]\n"
            f"[cyan]Welcome back, Elite Hacker.[/cyan]\n"
            f"[yellow]ID: {device_id}[/yellow]\n\n"
            f"[dim white]Logged in at: {current_time}[/dim white]\n"
            f"[bold magenta]Admin: Muhammad Shourov (Vampire)[/bold magenta]"
        )
        
        success_panel = Panel.fit(success_msg, title="[bold green]✔ ACCESS GRANTED[/bold green]", border_style="green", padding=(1, 2))
        console.print(Align.center(success_panel))
        
        time.sleep(1.5)
        return device_id  # ড্যাশবোর্ডের জন্য আইডি রিটার্ন করা হলো
    else:
        draw_denied_box(device_id)
        return None

# --- স্ট্যান্ডঅ্যালোন মেইন প্রোগ্রাম এক্সিকিউশন (ঐচ্ছিক টেস্টের জন্য) ---

if __name__ == "__main__":
    try:
        if verify_license():
            console.print(f"\n{BOLD}{GREEN}LAUNCHING VAMPIRE SQUAD TOOL...{RESET}")
            slow_print(f"{CYAN}Stay stealthy. Initializing modules...{RESET}", 0.05)
            # --- মূল কোডের লজিক ---
            
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Interrupted by user.{RESET}")
        sys.exit(0)
