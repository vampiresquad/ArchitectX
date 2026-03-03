# ui/visuals.py
import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner

# গ্লোবাল কনসোল অবজেক্ট
console = Console()

# =====================================================================
# [ ARCHITECTX CORE: BRANDING & CREDITS ]
# =====================================================================
AUTHOR = "Muhammad Shourov"
TEAM = "Vampire Squad"
VERSION = "2.0.0 (Enterprise Ultimate)"

def clear_screen():
    """ক্রস-প্ল্যাটফর্ম স্ক্রিন ক্লিয়ার (Termux, Linux, Mac, Windows)"""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_banner():
    """অত্যন্ত নিখুঁত এবং কালারফুল সাইবারপাঙ্ক ব্যানার"""
    banner = f"""
[bold cyan]    █████╗ ██████╗  ██████╗██╗  ██╗██╗████████╗███████╗ ██████╗████████╗██╗  ██╗[/bold cyan]
[bold cyan]   ██╔══██╗██╔══██╗██╔════╝██║  ██║██║╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝╚██╗██╔╝[/bold cyan]
[bold blue]   ███████║██████╔╝██║     ███████║██║   ██║   █████╗  ██║        ██║    ╚███╔╝ [/bold blue]
[bold blue]   ██╔══██║██╔══██╗██║     ██╔══██║██║   ██║   ██╔══╝  ██║        ██║    ██╔██╗ [/bold blue]
[bold magenta]   ██║  ██║██║  ██║╚██████╗██║  ██║██║   ██║   ███████╗╚██████╗   ██║   ██╔╝ ██╗[/bold magenta]
[bold magenta]   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝[/bold magenta]
    """
    
    credit_text = Text()
    credit_text.append(" " * 15)
    credit_text.append("© ALL RIGHTS RESERVED | DEVELOPED BY ", style="bold white")
    credit_text.append(AUTHOR, style="bold green blink")
    credit_text.append(f" (Founder of {TEAM})\n", style="bold yellow")
    credit_text.append(" " * 28 + f"Version: {VERSION}", style="dim cyan")

    console.print(banner)
    console.print(credit_text)
    console.print("\n")

# =====================================================================
# [ ARCHITECTX CORE: CUSTOM SPINNER ENGINE ]
# ইউজারের রিকোয়ারমেন্ট অনুযায়ী: স্কয়ার বক্সের ভেতর সার্কেল ডট [◉]
# =====================================================================
class VampireSpinner:
    def __init__(self, initial_text="Initializing Core..."):
        # কাস্টম ফ্রেম: স্কয়ার বক্সের ভেতর ঘুরতে থাকা সার্কেল ডট
        custom_frames = ["[ ◯ ]", "[ ◉ ]", "[ ● ]", "[ ◉ ]"]
        self.spinner = Spinner("dots", text=Text(initial_text, style="bold yellow"))
        # Rich এর ডিফল্ট স্পিনারকে ওভাররাইড করে কাস্টম ফ্রেম যুক্ত করা
        self.spinner.frames = custom_frames
        self.live = Live(self.spinner, refresh_per_second=10, transient=True)
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.live.start()
            self.is_running = True

    def update(self, text, style="bold cyan"):
        if self.is_running:
            self.spinner.text = Text(text, style=style)
            time.sleep(0.3) # ন্যাচারাল রিডিং ডিলে

    def stop(self, final_text, success=True):
        if self.is_running:
            self.live.stop()
            self.is_running = False
            if success:
                console.print(f"[bold green][ ✔ ] {final_text}[/bold green]")
            else:
                console.print(f"[bold red][ ✖ ] {final_text}[/bold red]")

# =====================================================================
# [ ARCHITECTX CORE: LIVE DASHBOARD PANEL ]
# =====================================================================
def render_dashboard(hwid_status="Verified", zai_status="Online", serper_status="Online"):
    """টার্মিনালে প্রফেশনাল স্প্লিট-স্ক্রিন ড্যাশবোর্ড দেখাবে"""
    
    # বাম দিকের প্যানেল: সিস্টেম ইনফো
    sys_info = Table.grid(padding=(0, 2))
    sys_info.add_row("[bold cyan]OS Platform:[/bold cyan]", f"[yellow]{sys.platform.upper()}[/yellow]")
    sys_info.add_row("[bold cyan]Engine:[/bold cyan]", "[yellow]ArchitectX Neural V2[/yellow]")
    sys_info.add_row("[bold cyan]Security:[/bold cyan]", "[green]Anti-Tamper Active[/green]")
    
    panel_left = Panel(sys_info, title="[bold magenta]System Node[/bold magenta]", border_style="cyan")

    # ডান দিকের প্যানেল: লাইভ নেটওয়ার্ক স্ট্যাটাস
    net_info = Table.grid(padding=(0, 2))
    
    hw_color = "bold green" if "Verified" in hwid_status else "bold red blink"
    net_info.add_row("[bold white]HWID License:[/bold white]", f"[{hw_color}]{hwid_status}[/{hw_color}]")
    
    zai_color = "bold green" if "Online" in zai_status else "bold yellow"
    net_info.add_row("[bold white]Z.ai Router:[/bold white]", f"[{zai_color}]{zai_status}[/{zai_color}]")
    
    serper_color = "bold green" if "Online" in serper_status else "bold yellow"
    net_info.add_row("[bold white]Serper API:[/bold white]", f"[{serper_color}]{serper_status}[/{serper_color}]")

    panel_right = Panel(net_info, title="[bold magenta]Network Status[/bold magenta]", border_style="cyan")

    # লেআউট তৈরি (স্ক্রিনকে দুই ভাগে ভাগ করা)
    layout = Layout()
    layout.split_row(
        Layout(panel_left, name="left"),
        Layout(panel_right, name="right")
    )
    
    console.print(layout)
    console.print("\n")
