# ui/visuals.py
import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from rich.align import Align

# গ্লোবাল কনসোল অবজেক্ট
console = Console()

# =====================================================================
# [ ARCHITECTX CORE: BRANDING & CREDITS ]
# =====================================================================
AUTHOR = "Muhammad Shourov"
TEAM = "Vampire Squad"
VERSION = "2.0.0 (Enterprise Ultimate)"

def clear_screen():
    """ক্রস-প্ল্যাটফর্ম স্ক্রিন ক্লিয়ার"""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_banner():
    """অত্যন্ত নিখুঁত এবং কালারফুল ব্যানার"""
    banner = f"""
[bold cyan]   █████╗ ██████╗  ██████╗██╗  ██╗██╗████████╗███████╗ ██████╗████████╗██╗  ██╗[/bold cyan]
[bold cyan]  ██╔══██╗██╔══██╗██╔════╝██║  ██║██║╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝╚██╗██╔╝[/bold cyan]
[bold blue]  ███████║██████╔╝██║     ███████║██║   ██║   █████╗  ██║        ██║    ╚███╔╝ [/bold blue]
[bold blue]  ██╔══██║██╔══██╗██║     ██╔══██║██║   ██║   ██╔══╝  ██║        ██║    ██╔██╗ [/bold blue]
[bold magenta]  ██║  ██║██║  ██║╚██████╗██║  ██║██║   ██║   ███████╗╚██████╗   ██║   ██╔╝ ██╗[/bold magenta]
[bold magenta]  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝[/bold magenta]
    """
    
    credit_text = Text()
    credit_text.append("© ALL RIGHTS RESERVED | DEVELOPED BY ", style="bold white")
    credit_text.append(AUTHOR, style="bold green blink")
    credit_text.append(f" (Founder of {TEAM})\n", style="bold yellow")
    credit_text.append(f"Version: {VERSION}", style="dim cyan")

    console.print(Align.center(banner))
    console.print(Align.center(credit_text))
    console.print("") # ছোট গ্যাপ

# =====================================================================
# [ ARCHITECTX CORE: CUSTOM SPINNER ENGINE ]
# =====================================================================
class VampireSpinner:
    def __init__(self, initial_text="Initializing Core..."):
        custom_frames = ["[ ◯ ]", "[ ◉ ]", "[ ● ]", "[ ◉ ]"]
        self.spinner = Spinner("dots", text=Text(initial_text, style="bold yellow"))
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
            time.sleep(0.3)

    def stop(self, final_text, success=True):
        if self.is_running:
            self.live.stop()
            self.is_running = False
            if success:
                console.print(f"[bold green][ ✔ ] {final_text}[/bold green]")
            else:
                console.print(f"[bold red][ ✖ ] {final_text}[/bold red]")

# =====================================================================
# [ ARCHITECTX CORE: COMPACT DASHBOARD PANEL ]
# =====================================================================
def render_dashboard(hwid_status="Verified", zai_status="Online", serper_status="Online"):
    """টার্মাক্স/মোবাইল ফ্রেন্ডলি স্লিক এবং কম্প্যাক্ট ড্যাশবোর্ড"""
    
    hw_color = "bold green" if "Verified" in hwid_status else "bold red blink"
    zai_color = "bold green" if "Online" in zai_status else "bold yellow"
    serper_color = "bold green" if "Online" in serper_status else "bold yellow"

    # এক বক্সের ভেতর সব ইনফরমেশন খুব গুছিয়ে দেওয়া হলো
    status_text = (
        f"[bold cyan]OS:[/bold cyan] [yellow]{sys.platform.upper()}[/yellow]   •   "
        f"[bold cyan]Engine:[/bold cyan] [yellow]V2 Core[/yellow]   •   "
        f"[bold cyan]Security:[/bold cyan] [green]Active[/green]\n"
        f"[bold white]HWID:[/bold white] [{hw_color}]{hwid_status}[/{hw_color}]   •   "
        f"[bold white]Z.ai:[/bold white] [{zai_color}]{zai_status}[/{zai_color}]   •   "
        f"[bold white]Serper:[/bold white] [{serper_color}]{serper_status}[/{serper_color}]"
    )

    panel = Panel(
        Align.center(status_text), 
        title="[bold magenta] SYSTEM STATUS MATRIX [/bold magenta]", 
        border_style="cyan",
        padding=(0, 2),
        expand=False # পুরো স্ক্রিন জুড়ে বক্স না করে টেক্সট অনুযায়ী ছোট বক্স করবে
    )

    console.print(Align.center(panel))
    console.print("") # মেনু আসার আগে একটি লাইন গ্যাপ
