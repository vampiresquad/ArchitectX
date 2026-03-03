#!/usr/bin/env python3
# ======================================================================
# [ ©ArchitectX 2.0 Enterprise - Developed by Muhammad Shourov ]
# [ ALL RIGHTS RESERVED | VAMPIRE SQUAD                        ]
# ======================================================================

import sys
import time
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

# UI Modules
from ui.visuals import clear_screen, draw_banner, render_dashboard, VampireSpinner
from ui.interact import get_main_menu_choice, interview_for_web, interview_for_tools, get_project_name

# Core Modules
from core.security import verify_license
from core.api_manager import APIRouter

# Engine Modules
from engines.scraper_x import scrape_target
from engines.ai_router import generate_code
from engines.compiler import compile_and_save, handle_hosting

def main():
    # ==========================================
    # 1. INITIALIZATION & SECURITY CHECK
    # ==========================================
    clear_screen()
    draw_banner()
    
    # স্পিনার ইনিশিয়ালাইজেশন
    master_spinner = VampireSpinner("Booting ArchitectX 2.0 Core Matrix...")
    master_spinner.start()
    time.sleep(1)
    
    # হার্ডওয়্যার লাইসেন্স ভেরিফিকেশন
    hwid = verify_license(master_spinner)
    if not hwid:
        sys.exit(1) # ভেরিফাই না হলে এখানেই বন্ধ হয়ে যাবে

    # এপিআই রাউটার ইনিশিয়ালাইজেশন
    master_spinner.start()
    router = APIRouter()
    api_status = router.initialize_engines(master_spinner)
    
    # ==========================================
    # 2. MAIN DASHBOARD LOOP
    # ==========================================
    while True:
        clear_screen()
        draw_banner()
        
        # লাইভ ড্যাশবোর্ড রেন্ডার
        render_dashboard(
            hwid_status=f"Verified ({hwid})", 
            zai_status=api_status['zai_status'], 
            serper_status=api_status['serper_status']
        )

        # মূল মেনু থেকে ইউজারের ইনপুট নেওয়া
        choice = get_main_menu_choice()
        
        if choice == "exit":
            master_spinner.start()
            master_spinner.update("Shutting down ArchitectX Neural Core...", style="red")
            time.sleep(1)
            master_spinner.stop("System disconnected. Stay stealthy, Vampire!")
            sys.exit(0)

        # ==========================================
        # 3. GRANULAR INTERVIEW & BLUEPRINT EXTRACTION
        # ==========================================
        project_name = get_project_name()
        project_type = "website" if choice == "clone" else choice
        user_prompt = ""

        if choice == "clone":
            target_url = inquirer.text(message="\nEnter the target URL to deep-clone (e.g., https://example.com):").execute()
            master_spinner.start()
            user_prompt = scrape_target(target_url, master_spinner)
            if not user_prompt:
                input("\nPress Enter to return to Dashboard...")
                continue
        elif choice in ["webapp", "website"]:
            user_prompt = interview_for_web(choice)
        elif choice == "tools":
            user_prompt = interview_for_tools()

        # ==========================================
        # 4. NEURAL GENERATION & COMPILATION
        # ==========================================
        master_spinner.start()
        
        # AI Router দিয়ে কোড জেনারেট করা
        code_dict = generate_code(project_type, user_prompt, api_status, master_spinner)
        
        if code_dict:
            master_spinner.start()
            # Compiler দিয়ে কোড সেভ, অটো-হিলিং এবং লাইসেন্স ইনজেক্ট করা
            compile_success = compile_and_save(project_name, project_type, code_dict, master_spinner)
            
            # ==========================================
            # 5. AUTO-HOSTING / DEPLOYMENT
            # ==========================================
            if compile_success and project_type in ["webapp", "website", "clone"]:
                print("\n[bold cyan]--- DEPLOYMENT ENGINE ---[/bold cyan]")
                hosting_choice = inquirer.select(
                    message="How would you like to deploy this workspace?",
                    choices=[
                        Choice(value="localhost", name="[ 1 ] Localhost Live Preview (Best for testing)"),
                        Choice(value="surge", name="[ 2 ] Global Live Deploy (Surge.sh CDN)"),
                        Choice(value="none", name="[ 0 ] Do nothing (Keep files locally)")
                    ]
                ).execute()
                
                if hosting_choice != "none":
                    master_spinner.start()
                    handle_hosting(project_name, hosting_choice, master_spinner)
                    
        else:
            print("\n[!] Project generation failed due to Neural core error.")

        # লুপ কন্টিনিউ করার আগে পজ
        input("\nPress Enter to return to the Main Command Center...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Emergency Override Triggered. Terminating System...")
        sys.exit(0)
