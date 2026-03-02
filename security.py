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

console = Console()

# আপনার অ্যাপ্রুভড লাইসেন্স লিস্টের লিংক (যেখানে আপনি পেইড ইউজারদের ID সেভ রাখবেন)
APPROVED_LIST_URL = "https://raw.githubusercontent.com/vampiresquad/Paid_Approval/refs/heads/main/approved.txt"

def get_hardware_id():
    """
    ইউজারের ডিভাইসের হার্ডওয়্যার ইনফরমেশন রিড করে একটি আন-চেঞ্জেবল ID তৈরি করে।
    """
    hw_id = ""
    system = platform.system()
    
    try:
        # Termux / Android এর জন্য
        if "ANDROID_ROOT" in os.environ or "PREFIX" in os.environ:
            hw_id = subprocess.check_output("settings get secure android_id", shell=True).decode().strip()
        # Windows এর জন্য
        elif system == "Windows":
            hw_id = subprocess.check_output("wmic csproduct get uuid", shell=True).decode().split('\n')[1].strip()
        # Linux / Mac (Darwin) এর জন্য
        elif system in ["Linux", "Darwin"]:
            hw_id = str(uuid.getnode())
        else:
            hw_id = str(uuid.getnode())
            
    except Exception:
        # কোনো কারণে ফেইল করলে ফলব্যাক হিসেবে MAC address নেবে
        hw_id = str(uuid.getnode())
        
    # আইডিটিকে সিকিউর এবং প্রফেশনাল লুক দেওয়ার জন্য SHA-256 এনক্রিপ্ট করে "VS-" যুক্ত করা হলো
    final_hwid = hashlib.sha256(hw_id.encode()).hexdigest()[:16]
    return f"VS-{final_hwid.upper()}"

def check_license():
    """
    লঞ্চ হওয়ার সময় ইউজারের ID চেক করে পারমিশন দেয় অথবা ব্লক করে দেয়।
    """
    console.print("\n[bold cyan]Initializing ArchitectX Premium Security System...[/bold cyan]")
    time.sleep(1)
    
    device_id = get_hardware_id()
    
    # সার্ভার থেকে অ্যাপ্রুভড লিস্ট আনা
    try:
        console.print("[yellow][*] Verifying License Key with Vampire Squad Servers...[/yellow]")
        response = requests.get(APPROVED_LIST_URL, timeout=10)
        if response.status_code == 200:
            approved_list = [line.strip() for line in response.text.splitlines() if line.strip()]
        else:
            approved_list = []
    except Exception as e:
        console.print("[bold red][!] Network Error: Could not connect to verification server.[/bold red]")
        sys.exit(1)

    # ভেরিফিকেশন লজিক
    time.sleep(0.5)
    if device_id in approved_list:
        # অ্যাক্সেস গ্র্যান্টেড প্যানেল
        success_text = f"[bold green]ACCESS GRANTED![/bold green]\n[cyan]Welcome back, Elite Hacker.[/cyan]\n[yellow]Device ID: {device_id}[/yellow]"
        console.print(Panel.fit(success_text, title="[bold green][ ArchitectX Core ][/bold green]", border_style="green", padding=(1, 2)))
        return True
    else:
        # অ্যাক্সেস ডিনাইড বক্স (আপনার আইডিয়া অনুযায়ী আরও প্রফেশনাল করা হয়েছে)
        denied_text = Text()
        denied_text.append(f"Device ID: {device_id}\n\n", style="bold cyan")
        denied_text.append("Contact the administrator (Muhammad Shourov) to request premium approval.\n", style="yellow")
        denied_text.append("You must provide the exact Device ID shown above.", style="bold red")
        
        console.print(Panel.fit(denied_text, title="[bold red]✖ ACCESS DENIED ✖[/bold red]", border_style="red", padding=(1, 2)))
        
        console.print("\n[magenta]Press Enter to exit. This message will remain logged.[/magenta]")
        try:
            input()
        except:
            pass
        sys.exit(1)

# টেস্ট করার জন্য
if __name__ == "__main__":
    check_license()
