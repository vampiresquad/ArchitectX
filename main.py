import os
import sys
import json
from rich.console import Console
from rich.panel import Panel
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

# আমাদের তৈরি করা কাস্টম মডিউলগুলো ইমপোর্ট করছি
import security
import ai_engine
import compiler
import scraper

console = Console()

def show_banner():
    """টার্মিনালে প্রফেশনাল হ্যাকার স্টাইলের ArchitectX ব্যানার শো করবে।"""
    banner = """
    █████╗ ██████╗  ██████╗██╗  ██╗██╗████████╗███████╗ ██████╗████████╗██╗  ██╗
   ██╔══██╗██╔══██╗██╔════╝██║  ██║██║╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝╚██╗██╔╝
   ███████║██████╔╝██║     ███████║██║   ██║   █████╗  ██║        ██║    ╚███╔╝ 
   ██╔══██║██╔══██╗██║     ██╔══██║██║   ██║   ██╔══╝  ██║        ██║    ██╔██╗ 
   ██║  ██║██║  ██║╚██████╗██║  ██║██║   ██║   ███████╗╚██████╗   ██║   ██╔╝ ██╗
   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝
    """
    console.print(f"[bold cyan]{banner}[/bold cyan]")
    console.print("[bold green]          Developed by Muhammad Shourov | Founder of Vampire Squad[/bold green]\n")

def load_or_get_api_key():
    """প্রথমবার ইউজারের কাছ থেকে Gemini API Key নিয়ে config.json এ সেভ রাখবে।"""
    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            try:
                config = json.load(f)
                if config.get("GEMINI_API_KEY"):
                    return config["GEMINI_API_KEY"]
            except:
                pass
    
    # যদি আগে থেকে সেভ করা না থাকে, তবে ইউজারের কাছে চাইবে
    console.print("[yellow][*] Gemini API Key not found. Initialization required.[/yellow]")
    api_key = inquirer.secret(message="Enter your Google Gemini API Key:").execute()
    
    with open(config_file, "w") as f:
        json.dump({"GEMINI_API_KEY": api_key}, f)
    console.print("[bold green][✔] API Key saved securely![/bold green]\n")
    return api_key

def main():
    # স্ক্রিন ক্লিয়ার করা
    os.system('cls' if os.name == 'nt' else 'clear')
    show_banner()

    # ধাপ ১: হার্ডওয়্যার আইডি এবং পেইড লাইসেন্স ভেরিফিকেশন
    security.check_license()

    # ধাপ ২: API Key লোড করা
    api_key = load_or_get_api_key()

    while True:
        # ধাপ ৩: ইন্টারেক্টিভ CLI মেনু
        choice = inquirer.select(
            message="Select an ArchitectX Module to launch:",
            choices=[
                Choice(value="webapp", name="1. Create Web App (Advanced functionality & logic)"),
                Choice(value="website", name="2. Create Website (Landing pages, Portfolios, etc.)"),
                Choice(value="tools", name="3. Create Tools (Python/Bash CLI utilities)"),
                Choice(value="clone", name="4. Clone from URL (Extract & Rebuild AI Replica)"),
                Choice(value="exit", name="5. Exit System")
            ],
            default="webapp"
        ).execute()

        if choice == "exit":
            console.print("\n[bold cyan][*] Shutting down ArchitectX Core. Stay stealthy, Vampire![/bold cyan]")
            sys.exit(0)

        # প্রজেক্টের নাম নেওয়া
        project_name = inquirer.text(message="Enter a name for your project (e.g., My_Vampire_Tool):").execute()
        project_name = project_name.strip().replace(" ", "_")

        user_prompt = ""

        # লজিক হ্যান্ডলিং
        if choice == "clone":
            target_url = inquirer.text(message="Enter the target website URL (e.g., https://example.com):").execute()
            # Scraper মডিউল কল করা
            blueprint = scraper.scrape_website(target_url)
            if not blueprint:
                continue
            user_prompt = blueprint
            project_type = "website" # ক্লোন করা সাইটগুলো ওয়েবসাইট হিসেবে সেভ হবে
        else:
            project_type = choice
            console.print("\n[yellow][*] Provide detailed requirements for your project.[/yellow]")
            console.print("[cyan](Example: I want a dark-themed hacking tool dashboard with a sidebar and a terminal-like window)[/cyan]")
            user_prompt = inquirer.text(message="Requirements:").execute()

        # ধাপ ৪: AI Engine-কে কল করে কোড জেনারেট করা
        code_dict = ai_engine.generate_code(project_type, user_prompt, api_key)

        if code_dict:
            # ধাপ ৫: Compiler-কে দিয়ে ফাইল সেভ করা এবং ArchitectX ক্রেডিট ইনজেক্ট করা
            compiler.compile_and_save(project_name, project_type, code_dict)
        
        console.print("\n[magenta]" + "="*60 + "[/magenta]\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold red][!] Process interrupted by user. Exiting ArchitectX...[/bold red]")
        sys.exit(0)
