import os
import platform
import subprocess
import hashlib
import uuid
import requests
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

console = Console()
APPROVED_LIST_URL = "https://raw.githubusercontent.com/vampiresquad/Paid_Approval/refs/heads/main/approved.txt"

def get_hardware_id():
    """ডিভাইসের আন-চেঞ্জেবল মাদারবোর্ড বা সিস্টেম আইডি রিড করে"""
    hw_id = ""
    system = platform.system()
    
    try:
        if "ANDROID_ROOT" in os.environ or "PREFIX" in os.environ:
            hw_id = subprocess.check_output("settings get secure android_id", shell=True).decode().strip()
        elif system == "Windows":
            hw_id = subprocess.check_output("wmic csproduct get uuid", shell=True).decode().split('\n')[1].strip()
        elif system in ["Linux", "Darwin"]:
            hw_id = str(uuid.getnode())
        else:
            hw_id = str(uuid.getnode())
    except Exception:
        hw_id = str(uuid.getnode())
        
    final_hwid = hashlib.sha256(hw_id.encode()).hexdigest()[:16]
    return f"VS-{final_hwid.upper()}"

def draw_denied_box(device_id):
    """অ্যাক্সেস ডিনাইড হলে প্রফেশনাল হ্যাকার বক্স দেখাবে"""
    denied_text = Text()
    denied_text.append(f"Device ID: {device_id}\n\n", style="bold cyan")
    denied_text.append("STATUS: UNAUTHORIZED\n", style="bold red blink")
    denied_text.append("Contact the administrator (Muhammad Shourov) to request premium approval.\n", style="yellow")
    denied_text.append("You must provide the exact Device ID shown above.", style="bold white")
    
    console.print(Panel.fit(
        denied_text, 
        title="[bold red]✖ SYSTEM LOCKDOWN ✖[/bold red]", 
        border_style="red", 
        padding=(1, 3)
    ))
    console.print("\n[magenta]Press Enter to terminate connection...[/magenta]")
    try:
        input()
    except:
        pass
    sys.exit(1)

def verify_license():
    """পেইড লাইসেন্স চেকার এবং ভেরিফিকেশন ইঞ্জিন"""
    console.print("\n[bold cyan]Initializing ArchitectX Premium Security Protocol...[/bold cyan]")
    time.sleep(0.5)
    device_id = get_hardware_id()
    
    try:
        with console.status("[yellow]Authenticating Device with Vampire Squad Servers...[/yellow]", spinner="aesthetic"):
            response = requests.get(APPROVED_LIST_URL, timeout=12)
            if response.status_code == 200:
                approved_list = [line.strip() for line in response.text.splitlines() if line.strip()]
            else:
                approved_list = []
    except Exception as e:
        console.print("[bold red][!] Network Error: Shield activated. Could not connect to auth server.[/bold red]")
        sys.exit(1)

    if device_id in approved_list:
        success_text = f"[bold green]AUTHENTICATION SUCCESSFUL[/bold green]\n[cyan]Welcome to the command center, Elite Hacker.[/cyan]\n[yellow]Device ID: {device_id}[/yellow]"
        console.print(Panel.fit(success_text, title="[bold green][ ArchitectX Core Active ][/bold green]", border_style="green", padding=(1, 2)))
        return True
    else:
        draw_denied_box(device_id)
        return False

if __name__ == "__main__":
    verify_license()
