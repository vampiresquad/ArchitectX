import os
import time
from rich.console import Console

# Rich লাইব্রেরি দিয়ে টার্মিনালে সুন্দর কালারফুল আউটপুট দেখানোর জন্য
console = Console()

def inject_architectx_credit(code_content, project_type):
    """
    AI-এর জেনারেট করা কোডে ArchitectX-এর ক্রেডিট এবং Security Guard যুক্ত করে।
    """
    if project_type.lower() in ['website', 'webapp']:
        # HTML/JS Anti-Tamper Mechanism
        html_credit = """
<div id="architectx-auth-layer" style="background-color: #0d1117; color: #00ff00; padding: 10px 15px; font-family: 'Courier New', Courier, monospace; font-size: 13px; text-align: right; border-top: 1px solid #00ff00; position: fixed; bottom: 0; right: 0; width: 100%; z-index: 999999;">
    [©ArchitectX - Developed by Muhammed Shourov<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Founder of "Vampire Squad" ]
</div>
<script>
// Anti-Tamper Security by ArchitectX Core
setInterval(function() {
    var creditLayer = document.getElementById('architectx-auth-layer');
    // চেক করবে ক্রেডিট ডিভ আছে কিনা, টেক্সট মুছেছে কিনা বা CSS দিয়ে হাইড করেছে কিনা
    if (!creditLayer || creditLayer.innerHTML.length < 50 || window.getComputedStyle(creditLayer).display === 'none' || window.getComputedStyle(creditLayer).opacity == 0) {
        document.body.innerHTML = '<div style="background:#0d1117;color:#ff0000;height:100vh;display:flex;align-items:center;justify-content:center;font-family:monospace;font-size:22px;text-align:center;">[!] FATAL ERROR: ArchitectX Core License Removed or Tampered.<br>Access Denied.</div>';
    }
}, 2000);
</script>
"""
        # কোডের </body> ট্যাগের ঠিক আগে ক্রেডিট ইনজেক্ট করবে
        if "</body>" in code_content:
            return code_content.replace("</body>", html_credit + "\n</body>")
        else:
            return code_content + html_credit

    elif project_type.lower() == 'tools':
        # Python বা Bash স্ক্রিপ্টের জন্য আন-রিমুভেবল ব্যানার
        banner = """#!/usr/bin/env python3
# ======================================================================
# [©ArchitectX - Developed by Muhammed Shourov
#                                        Founder of "Vampire Squad" ]
# ======================================================================
# WARNING: Removing this core license may cause functional failures.
"""
        return banner + "\n" + code_content
        
    return code_content

def compile_and_save(project_name, project_type, code_dict):
    """
    AI থেকে পাওয়া কোডগুলো ফোল্ডারে গুছিয়ে সেভ করবে।
    code_dict: {'index.html': '<html>...', 'style.css': 'body{...}'}
    """
    console.print(f"\n[bold yellow][*] Injecting ArchitectX Core License for '{project_name}'...[/bold yellow]")
    time.sleep(1)
    
    # প্রজেক্টের নামে নতুন ফোল্ডার তৈরি
    if not os.path.exists(project_name):
        os.makedirs(project_name)
        
    # প্রতিটি ফাইল প্রসেস ও সেভ করা
    for filename, content in code_dict.items():
        filepath = os.path.join(project_name, filename)
        
        # শুধুমাত্র মূল ফাইলগুলোতে (html বা python/bash) ক্রেডিট ইনজেক্ট করবে
        if filename.endswith('.html') or filename == 'main.py' or filename.endswith('.sh'):
            content = inject_architectx_credit(content, project_type)
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        console.print(f"[bold green][+] Compiled successfully: {filename}[/bold green]")
        
    console.print(f"\n[bold cyan][✔] Project '{project_name}' successfully compiled and secured![/bold cyan]")
    console.print(f"[cyan]Saved at: {os.path.abspath(project_name)}[/cyan]\n")
    return True
