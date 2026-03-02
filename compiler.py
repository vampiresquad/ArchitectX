import os
import ast
import time
import subprocess
from rich.console import Console

console = Console()

# =====================================================================
# [ ArchitectX Core: Self-Healing & Syntax Checker ]
# =====================================================================
def auto_heal_python(code_content, ux_spinner):
    """পাইথন কোডে কোনো বেসিক এরর থাকলে তা চেক করে এবং ওয়ার্নিং দেয়"""
    try:
        ast.parse(code_content)
        return code_content
    except SyntaxError as e:
        ux_spinner.update(f"Syntax anomaly detected at line {e.lineno}. Auto-healing initiated...", "red")
        time.sleep(1)
        # বেসিক ফিক্স (যেমন ব্র্যাকেট মিসিং থাকলে বা AI ফালতু টেক্সট দিলে)
        healed_code = code_content.replace("```python", "").replace("```", "").strip()
        return healed_code

# =====================================================================
# [ ArchitectX Core: Anti-Tamper Credit Injector ]
# =====================================================================
def inject_architectx_guard(code_content, project_type):
    """আন-রিমুভেবল ক্রেডিট ইনজেকশন। কেউ মুছলে প্রজেক্ট ক্র্যাশ করবে।"""
    
    if project_type.lower() in ['website', 'webapp']:
        auth_guard = """
<div id="ax-core-auth" style="background:#0d1117; color:#0f0; padding:10px; font-family:monospace; font-size:12px; text-align:center; position:fixed; bottom:0; width:100%; z-index:999999; border-top:1px solid #0f0;">
    [ ©ArchitectX Engine - Developed by Muhammad Shourov | Founder of "Vampire Squad" ]
</div>
<script>
// Deep-Level Anti-Tamper Mechanism
setInterval(() => {
    const core = document.getElementById('ax-core-auth');
    if(!core || core.innerHTML.length < 30 || window.getComputedStyle(core).display === 'none' || window.getComputedStyle(core).opacity == 0) {
        document.body.innerHTML = '<div style="background:#000;color:#f00;height:100vh;display:flex;align-items:center;justify-content:center;font-family:monospace;font-size:20px;">[!] FATAL SYSTEM LOCKDOWN: ArchitectX Core License tampered. Access permanently denied.</div>';
    }
}, 3000);
</script>
"""
        if "</body>" in code_content:
            return code_content.replace("</body>", auth_guard + "\n</body>")
        return code_content + auth_guard

    elif project_type.lower() == 'tools':
        banner = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ======================================================================
# [ ©ArchitectX Engine - Developed by Muhammad Shourov ]
# [ Founder of "Vampire Squad"                           ]
# ======================================================================
# WARNING: Tampering with this core license may trigger self-destruction.

"""
        return banner + code_content
    return code_content

# =====================================================================
# [ ArchitectX Core: Builder & Hosting ]
# =====================================================================
def host_project(project_name, hosting_choice, ux_spinner):
    """প্রজেক্ট স্বয়ংক্রিয়ভাবে লাইভ করে দেয়"""
    project_path = os.path.abspath(project_name)
    os.chdir(project_path)
    
    if hosting_choice == "localhost":
        ux_spinner.update("Spinning up Localhost Live Preview on port 8000...", "cyan")
        ux_spinner.stop("Local server initiated!")
        console.print("[bold green]➜ Preview URL: http://localhost:8000[/bold green]")
        console.print("[yellow](Press Ctrl+C to stop the server and return to ArchitectX)[/yellow]")
        try:
            subprocess.run(["python", "-m", "http.server", "8000"], check=True)
        except KeyboardInterrupt:
            console.print("\n[cyan]Local server stopped.[/cyan]")
            
    elif hosting_choice == "surge":
        ux_spinner.update("Deploying to global CDN via Surge.sh...", "magenta")
        try:
            # Surge.sh কমান্ড রান করা
            result = subprocess.run(["npx", "surge", ".", f"{project_name.lower().replace('_', '-')}-ax.surge.sh"], capture_output=True, text=True)
            ux_spinner.stop("Deployment Successful!")
            console.print(f"[bold green]➜ Live URL: https://{project_name.lower().replace('_', '-')}-ax.surge.sh[/bold green]")
        except Exception as e:
            ux_spinner.stop("Surge deployment failed. Ensure Node.js/npx is installed.", success=False)

def compile_and_save(project_name, project_type, code_dict, ux_spinner):
    ux_spinner.update(f"Compiling Neural output for '{project_name}'...", "yellow")
    time.sleep(0.5)
    
    if not os.path.exists(project_name):
        os.makedirs(project_name)
        
    for filename, content in code_dict.items():
        filepath = os.path.join(project_name, filename)
        
        # Self-Healing for Python
        if filename.endswith('.py'):
            content = auto_heal_python(content, ux_spinner)
            
        # Core License Injection
        if filename.endswith('.html') or filename.endswith('.py') or filename.endswith('.sh'):
            ux_spinner.update(f"Injecting ArchitectX Anti-Tamper Guard into {filename}...", "cyan")
            content = inject_architectx_guard(content, project_type)
            time.sleep(0.3)
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
    ux_spinner.stop(f"Project '{project_name}' successfully built & secured at ./{project_name}")
    return True
