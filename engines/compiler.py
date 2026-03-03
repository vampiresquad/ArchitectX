#!/usr/bin/env python3
# ======================================================================
# [ ©ArchitectX 2.0 Enterprise - Developed by Muhammad Shourov ]
# [ ALL RIGHTS RESERVED | VAMPIRE SQUAD                        ]
# ======================================================================

import os
import ast
import time
import subprocess
from rich.console import Console

console = Console()

def auto_heal_python(code_content, spinner_engine):
    """পাইথন কোডের সিনট্যাক্স স্ক্যান করে অটো-হিলিং (Auto-heal) করে"""
    try:
        ast.parse(code_content)
        return code_content
    except SyntaxError as e:
        spinner_engine.update(f"Syntax anomaly at line {e.lineno}. Auto-healing code...", style="yellow")
        time.sleep(0.5)
        return code_content.replace("```python", "").replace("```", "").strip()

def inject_author_credits(code_content, project_type):
    """১০০% নিখুঁত এবং আন-রিমুভেবল Vampire Squad ক্রেডিট ইনজেকশন"""
    
    if project_type in ['website', 'webapp', 'clone']:
        auth_guard = """
<div id="vs-auth-core" style="background:#000; color:#0f0; padding:10px; font-family:monospace; font-size:12px; text-align:center; position:fixed; bottom:0; width:100%; z-index:999999; border-top:1px solid #0f0;">
    [ ©ArchitectX 2.0 - Developed by Muhammad Shourov | Founder of Vampire Squad ]
</div>
<script>
// Deep Anti-Tamper Core
setInterval(() => {
    const core = document.getElementById('vs-auth-core');
    if(!core || window.getComputedStyle(core).display === 'none' || core.innerHTML.length < 20) {
        document.body.innerHTML = '<div style="background:#000;color:#f00;height:100vh;display:flex;align-items:center;justify-content:center;font-family:monospace;font-size:22px;">[!] FATAL ERROR: ArchitectX License Tampered.</div>';
    }
}, 3000);
</script>
"""
        if "</body>" in code_content:
            return code_content.replace("</body>", auth_guard + "\n</body>")
        return code_content + auth_guard

    elif project_type == 'tools':
        banner = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ======================================================================
# [ ©ArchitectX 2.0 Enterprise - Developed by Muhammad Shourov ]
# [ Founder of "Vampire Squad" | ALL RIGHTS RESERVED           ]
# ======================================================================
# WARNING: Tampering with this core license may trigger system lockdown.

"""
        return banner + code_content
    return code_content

def compile_and_save(project_name, project_type, code_dict, spinner_engine):
    """ডিকশনারি থেকে কোডগুলো রিড করে ফোল্ডার এবং ফাইল তৈরি করে"""
    spinner_engine.update(f"Compiling Neural Output for '{project_name}'...", style="yellow")
    
    if not os.path.exists(project_name):
        os.makedirs(project_name)
        
    for filename, content in code_dict.items():
        filepath = os.path.join(project_name, filename)
        
        # Self-Healing
        if filename.endswith('.py'):
            content = auto_heal_python(content, spinner_engine)
            
        # Author Injector
        if filename.endswith(('.html', '.py', '.sh', '.js')):
            spinner_engine.update(f"Injecting Vampire Squad Anti-Tamper Guard into {filename}...", style="cyan")
            content = inject_author_credits(content, project_type)
            time.sleep(0.2)
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
    # ArchitectX প্রজেক্ট মেটাডেটা সেভ করা
    with open(os.path.join(project_name, ".architectx"), "w") as f:
        f.write(f"Version: 2.0\nType: {project_type}\nAuthor: Muhammad Shourov")

    spinner_engine.stop(f"Project Workspace '{project_name}' built & secured successfully!")
    return True

def handle_hosting(project_name, hosting_choice, spinner_engine):
    """লোকালহোস্ট বা Surge.sh এর মাধ্যমে অটো-হোস্টিং"""
    project_path = os.path.abspath(project_name)
    os.chdir(project_path)
    
    if hosting_choice == "localhost":
        spinner_engine.update("Spinning up Localhost Live Preview on port 8000...", style="cyan")
        spinner_engine.stop("Local server initiated!")
        console.print("[bold green]➜ Preview URL: http://localhost:8000[/bold green]")
        console.print("[yellow](Press Ctrl+C to stop the server and return)[/yellow]")
        try:
            subprocess.run(["python", "-m", "http.server", "8000"], check=True)
        except KeyboardInterrupt:
            console.print("\n[cyan]Local server stopped.[/cyan]")
            
    elif hosting_choice == "surge":
        spinner_engine.update("Deploying to global CDN via Surge.sh...", style="magenta")
        try:
            domain_name = f"{project_name.lower().replace('_', '-')}-vs-core.surge.sh"
            subprocess.run(["npx", "surge", ".", domain_name], capture_output=True, text=True)
            spinner_engine.stop("Deployment Successful!")
            console.print(f"[bold green]➜ Live URL: https://{domain_name}[/bold green]")
        except Exception:
            spinner_engine.stop("Surge deployment failed. Ensure Node.js/npx is installed.", success=False)
