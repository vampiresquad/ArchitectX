import json
import requests
from rich.console import Console

console = Console()

# এথিক্যাল ফিল্টারের জন্য ডার্ক কিউয়ার্ড লিস্ট (আপনি চাইলে আরও শব্দ যোগ করতে পারেন)
BLOCKED_KEYWORDS = [
    "ddos", "ransomware", "phishing", "malware", "virus", 
    "exploit", "hack bank", "steal password", "trojan", "keylogger"
]

def ethical_check(prompt):
    """
    ইউজারের ইনপুট স্ক্যান করে অনৈতিক কাজের রিকোয়েস্ট ব্লক করে।
    """
    prompt_lower = prompt.lower()
    for word in BLOCKED_KEYWORDS:
        if word in prompt_lower:
            return False, word
    return True, None

def generate_code(project_type, user_prompt, api_key):
    """
    Gemini API ব্যবহার করে ইউজারের ইনপুট অনুযায়ী কোড জেনারেট করে 
    এবং আউটপুটটিকে JSON ডিকশনারিতে কনভার্ট করে।
    """
    # ১. এথিক্যাল ফিল্টার চেক
    is_ethical, bad_word = ethical_check(user_prompt)
    
    if not is_ethical:
        console.print(f"\n[bold red][!] SECURITY ALERT: Unethical request detected (Keyword: '{bad_word}').[/bold red]")
        console.print("[red]ArchitectX can only be used for legal and ethical purposes.[/red]")
        return None

    console.print(f"\n[bold yellow][*] ArchitectX AI Engine Processing your {project_type}...[/bold yellow]")
    
    # ২. প্রম্পট ইঞ্জিনিয়ারিং (AI-কে নির্দিষ্ট ফরম্যাটে কোড দেওয়ার কড়া নির্দেশ)
    system_instruction = f"""
    You are ArchitectX, an elite, professional code generator developed by Muhammad Shourov (Vampire Squad).
    The user wants to create a {project_type}.
    User detailed requirements: {user_prompt}
    
    CRITICAL RULES FOR OUTPUT:
    1. Return ONLY a valid JSON object. No markdown formatting, no explanations, no ```json tags.
    2. The keys of the JSON must be the exact filenames (e.g., 'index.html', 'style.css', 'script.js' or 'main.py').
    3. The values must be the complete, fully functional, production-ready code for that specific file.
    4. Ensure modern UI/UX for web projects and clean, commented code for tools.
    """

    # ৩. API রিকোয়েস্ট সেটআপ (Gemini 1.5 Flash API)
    url = f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=](https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=){api_key}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": system_instruction}]}],
        "generationConfig": {
            # এটি AI-কে বাধ্য করবে শুধুমাত্র JSON আউটপুট দিতে
            "response_mime_type": "application/json", 
        }
    }

    # ৪. AI-এর সাথে কানেকশন তৈরি
    try:
        console.print("[cyan][*] Connecting to ArchitectX Neural Core (Powered by Gemini)...[/cyan]")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result['candidates'][0]['content']['parts'][0]['text']
        
        # ৫. স্ট্রিং থেকে JSON ডিকশনারিতে রূপান্তর
        code_dict = json.loads(generated_text)
        console.print("[bold green][✔] Code structure generated successfully![/bold green]")
        return code_dict
        
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red][!] API Connection Error: Check your internet connection or API Key.[/bold red]")
        return None
    except json.JSONDecodeError:
        console.print("[bold red][!] AI provided an invalid format. Retrying is recommended.[/bold red]")
        return None
    except Exception as e:
        console.print(f"[bold red][!] Unknown Error in AI Engine: {e}[/bold red]")
        return None
