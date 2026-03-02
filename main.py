import os
import sys
import json
from rich.console import Console
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

import security
from api_manager import APIRouter, ArchitectXSpinner
import ai_engine
import scraper
import compiler

console = Console()
CONFIG_FILE = "architectx_config.json"

def show_banner():
    banner = """
    █████╗ ██████╗  ██████╗██╗  ██╗██╗████████╗███████╗ ██████╗████████╗██╗  ██╗
   ██╔══██╗██╔══██╗██╔════╝██║  ██║██║╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝╚██╗██╔╝
   ███████║██████╔╝██║     ███████║██║   ██║   █████╗  ██║        ██║    ╚███╔╝ 
   ██╔══██║██╔══██╗██║     ██╔══██║██║   ██║   ██╔══╝  ██║        ██║    ██╔██╗ 
   ██║  ██║██║  ██║╚██████╗██║  ██║██║   ██║   ███████╗╚██████╗   ██║   ██╔╝ ██╗
   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝
    """
    console.print(f"[bold cyan]{banner}[/bold cyan]")
    console.print("[bold green]     >> ENFORCED BY MUHAMMAD SHOUROV | FOUNDER OF VAMPIRE SQUAD <<[/bold green]\n")

def load_config():
    """ইউজারের API Config লোড বা তৈরি করে"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"ZAI_KEY": "", "SERPER_KEY": ""}

def granular_interview(project_type):
    """ইউজারের কাছ থেকে ধাপে ধাপে (Tree Structure) নিখুঁত রিকোয়ারমেন্টস নেয়"""
    console.print(f"\n[bold yellow]--- ArchitectX Project Wizard ({project_type.upper()}) ---[/bold yellow]")
    
    if project_type in ["webapp", "website"]:
        core_func = inquirer.text(message="1. What is the core function? (e.g., Notepad, Portfolio, Dashboard):").execute()
        sections = inquirer.text(message="2. What sections do you need? (e.g., Home, About, Login, Admin Panel):").execute()
        theme = inquirer.select(
            message="3. Select a Color Theme:",
            choices=["Cyberpunk Dark (Green/Black)", "Modern Light (Blue/White)", "Dracula Dark (Purple/Grey)", "Custom"]
        ).execute()
        if theme == "Custom":
            theme = inquirer.text(message="Describe your custom colors:").execute()
            
        db_setup = inquirer.confirm(message="4. Do you need Backend/Database placeholders (Firebase/Supabase)?").execute()
        
        prompt = f"Core: {core_func}. Sections: {sections}. Theme: {theme}. Database setup needed: {db_setup}."
        
    elif project_type == "tools":
        core_func = inquirer.text(message="1. What does this tool do? (e.g., IP Tracker, File Encryptor):").execute()
        interface = inquirer.select(message="2. Interface type:", choices=["CLI (Command Line)", "GUI (Tkinter/PyQt)"]).execute()
        features = inquirer.text(message="3. List specific features (comma separated):").execute()
        
        prompt = f"Core: {core_func}. Interface: {interface}. Features: {features}."
        
    return prompt

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    show_banner()

    # 1. Gatekeeper / Hardware Security
    security.verify_license()

    # 2. API Routing & Health Check
    user_config = load_config()
    router = APIRouter()
    active_apis = router.initialize_engines(user_config)

    while True:
        # 3. Core Matrix Menu
        choice = inquirer.select(
            message="[ ArchitectX Command Center ] Select operation:",
            choices=[
                Choice(value="webapp", name="1. 🚀 Generate Web App (Dynamic logic, BaaS)"),
                Choice(value="website", name="2. 🌐 Generate Website (Landing, Portfolio)"),
                Choice(value="tools", name="3. ⚙️ Generate Tool (Python/Bash Scripts)"),
                Choice(value="clone", name="4. 🧬 Deep Clone URL (Extract & Rebuild)"),
                Choice(value="exit", name="5. ✖️ Terminate System")
            ]
        ).execute()

        if choice == "exit":
            console.print("\n[bold red]Shutting down ArchitectX Neural Core... Stay Stealthy.[/bold red]")
            sys.exit(0)

        project_name = inquirer.text(message="Enter Project/Folder Name:").execute().strip().replace(" ", "_")

        # 4. Granular Input & Scraper
        if choice == "clone":
            target_url = inquirer.text(message="Enter target URL to clone:").execute()
            ux_spinner = ArchitectXSpinner()
            ux_spinner.start()
            user_prompt = scraper.scrape_website(target_url, ux_spinner)
            if not user_prompt:
                continue
            project_type = "website"
        else:
            project_type = choice
            user_prompt = granular_interview(project_type)

        # 5. AI Generation
        ux_spinner = ArchitectXSpinner()
        ux_spinner.start()
        code_dict = ai_engine.generate_code(project_type, user_prompt, active_apis, ux_spinner)

        # 6. Compilation & Injection
        if code_dict:
            ux_spinner.start()
            if compiler.compile_and_save(project_name, project_type, code_dict, ux_spinner):
                
                # 7. Auto-Hosting System
                console.print("\n[bold cyan]--- Deployment Engine ---[/bold cyan]")
                host_choice = inquirer.select(
                    message="How would you like to run/host this project?",
                    choices=[
                        Choice(value="localhost", name="1. Live Preview (Localhost) - Recommended for testing"),
                        Choice(value="surge", name="2. Global Hosting (Surge.sh) - Best for static Web/Apps"),
                        Choice(value="none", name="3. Do nothing (Keep files locally)")
                    ]
                ).execute()
                
                if host_choice != "none":
                    ux_spinner.start()
                    compiler.host_project(project_name, host_choice, ux_spinner)
                    
        console.print("\n[magenta]" + "═"*70 + "[/magenta]\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold red][!] Emergency override triggered. Exiting ArchitectX...[/bold red]")
        sys.exit(0)
