# ui/interact.py
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator
from rich.console import Console

console = Console()

# =====================================================================
# [ ARCHITECTX CORE: GRANULAR INTERVIEW SYSTEM ]
# কীবোর্ড এবং কার্সার সাপোর্ট সহ স্টেপ-বাই-স্টেপ ডিটেইলস কালেক্টর
# =====================================================================

def get_main_menu_choice():
    """মূল মেনু: ইউজার কী তৈরি করতে চায়?"""
    console.print("[bold yellow]➤ SELECT OPERATION PROTOCOL:[/bold yellow]")
    choice = inquirer.select(
        message="Use Arrow Keys or Mouse Cursor to select:",
        choices=[
            Choice(value="webapp", name="[ 1 ] 🚀 Full-Stack Web App (Dynamic Logic, API, Database)"),
            Choice(value="website", name="[ 2 ] 🌐 Static Website (Landing Page, Portfolio, Blog)"),
            Choice(value="tools", name="[ 3 ] ⚙️ Premium Tool/Script (Python, Bash, Utilities)"),
            Choice(value="clone", name="[ 4 ] 🧬 Deep Clone Engine (Extract UI from URL)"),
            Choice(value="exit", name="[ 0 ] ✖️ Terminate Connection")
        ],
        pointer="❯",
    ).execute()
    return choice

def interview_for_web(project_type):
    """ওয়েব অ্যাপ বা ওয়েবসাইটের জন্য একদম গুছানো ইনপুট"""
    console.print(f"\n[bold cyan]--- {project_type.upper()} ARCHITECTURE WIZARD ---[/bold cyan]")
    
    core_concept = inquirer.text(
        message="1. Core Concept (e.g., 'A note-taking app', 'Hacker portfolio'):",
        validate=EmptyInputValidator("Concept cannot be empty!")
    ).execute()
    
    pages = inquirer.text(
        message="2. Required Sections/Pages (e.g., 'Home, About, Dashboard, Login'):",
        default="Home, About, Contact"
    ).execute()

    theme = inquirer.select(
        message="3. Select Base Color Typography/Theme:",
        choices=[
            "Cyberpunk (Neon Green, Black, Matrix vibe)",
            "Dracula (Dark Grey, Purple, Pink)",
            "Corporate Clean (White, Light Blue, Minimalist)",
            "Vampire Dark (Deep Red, Pitch Black, Elite)"
        ]
    ).execute()

    functionality = inquirer.text(
        message="4. Special Features (e.g., 'Animations, Dark mode toggle, working contact form'):"
    ).execute()

    return f"Concept: {core_concept}. Sections: {pages}. Theme: {theme}. Features: {functionality}."

def interview_for_tools():
    """পাইথন বা ব্যাশ টুল বানানোর জন্য স্পেসিফিক ইনপুট"""
    console.print(f"\n[bold cyan]--- PREMIUM TOOL/SCRIPT WIZARD ---[/bold cyan]")
    
    tool_purpose = inquirer.text(
        message="1. What will this tool do? (e.g., 'Port scanner', 'File encryptor'):",
        validate=EmptyInputValidator("Tool purpose is required!")
    ).execute()

    ui_type = inquirer.select(
        message="2. Select Tool Interface Type:",
        choices=["CLI (Command Line with Rich colors)", "GUI (Tkinter/PyQt window)", "Background Service (No UI)"]
    ).execute()

    os_support = inquirer.checkbox(
        message="3. Select Target OS (Space to select, Enter to confirm):",
        choices=["Termux/Android", "Linux/Ubuntu", "macOS", "Windows"],
        validate=lambda result: len(result) >= 1,
        invalid_message="Must select at least one OS!"
    ).execute()

    return f"Purpose: {tool_purpose}. Interface: {ui_type}. Supported OS: {', '.join(os_support)}."

def get_project_name():
    """প্রজেক্টের নাম ফোল্ডার ফ্রেন্ডলি করে নেবে"""
    name = inquirer.text(
        message="\nEnter Project/Folder Name (Spaces will be converted to underscores):",
        validate=EmptyInputValidator("Project name cannot be empty!")
    ).execute()
    return name.strip().replace(" ", "_")
