#!/usr/bin/env python3
# ======================================================================
# [ ©ArchitectX 2.0 Enterprise - Developed by Muhammad Shourov ]
# [ ALL RIGHTS RESERVED | VAMPIRE SQUAD                        ]
# ======================================================================

import requests
from bs4 import BeautifulSoup
import re
from rich.console import Console

console = Console()

def extract_colors(html_content):
    """HTML থেকে আধুনিক রেগুলার এক্সপ্রেশন ব্যবহার করে কালার কোড বের করে"""
    hex_colors = re.findall(r'#(?:[0-9a-fA-F]{3}){1,2}\b', html_content)
    return list(set(hex_colors))[:6] # সেরা ৬টি ইউনিক কালার

def scrape_target(url, spinner_engine):
    """ওয়েবসাইটের UI/UX DNA রিড করার এন্টারপ্রাইজ ফাংশন"""
    spinner_engine.update(f"Initiating Deep-Clone Protocol for: {url}", style="yellow")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ArchitectX-DeepClone/2.0',
            'Accept': 'text/html,application/xhtml+xml'
        }
        
        spinner_engine.update("Bypassing firewalls & fetching DOM...", style="cyan")
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        spinner_engine.update("Extracting UI patterns & Color Palettes...", style="magenta")
        color_palette = extract_colors(html_content)
        
        # ক্লিন স্ট্রাকচার পাওয়ার জন্য স্ক্রিপ্ট বাদ দেওয়া
        for script in soup(["script", "style", "noscript", "meta", "svg", "img"]):
            script.extract()
            
        title = soup.title.string.strip() if soup.title else "ArchitectX Cloned Project"
        nav_links = [a.get_text(strip=True) for a in soup.find_all('a') if len(a.get_text(strip=True)) > 2][:6]
        buttons = [b.get_text(strip=True) for b in soup.find_all(['button', 'a']) if 'btn' in b.get('class', []) or 'button' in b.get('class', [])][:5]
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2']) if h.get_text(strip=True)][:5]
        
        spinner_engine.stop("Target DNA successfully sequenced!")
        
        # AI-এর জন্য মাস্টার ব্লুপ্রিন্ট
        blueprint = f"""
        CLONE TARGET DATA:
        - Original Title: {title}
        - Color Palette to Use: {', '.join(color_palette) if color_palette else 'Modern Dark Tech Theme'}
        - Navigation Items: {', '.join(nav_links)}
        - Call-to-Actions (Buttons): {', '.join(buttons)}
        - Main Structural Headings: {', '.join(headings)}
        
        CRITICAL INSTRUCTION: Rebuild this exact website structure. Use the discovered colors. Ensure the UI is 100% responsive, modern, and professional.
        """
        return blueprint

    except requests.exceptions.MissingSchema:
        spinner_engine.stop("Invalid URL format (Must include http/https).", success=False)
        return None
    except Exception as e:
        spinner_engine.stop(f"Clone engine failure: {e}", success=False)
        return None
