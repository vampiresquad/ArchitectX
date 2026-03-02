import requests
from bs4 import BeautifulSoup
import re
from rich.console import Console

console = Console()

# =====================================================================
# [ ArchitectX Core: Deep Web Cloning Module ]
# =====================================================================
def extract_colors(html_content):
    """HTML এবং ইনলাইন CSS থেকে হেক্স কালার কোডগুলো খুঁজে বের করে"""
    hex_colors = re.findall(r'#(?:[0-9a-fA-F]{3}){1,2}\b', html_content)
    # ডুপ্লিকেট বাদ দিয়ে প্রথম ৫টি ইউনিক কালার নেওয়া
    return list(set(hex_colors))[:5]

def scrape_website(url, ux_spinner):
    """
    যেকোনো ওয়েবসাইটের একদম গভীরে গিয়ে তার DNA (ডিজাইন স্ট্রাকচার) রিড করে।
    """
    ux_spinner.update(f"Initiating Deep-Clone Protocol for: {url}", "yellow")
    
    try:
        # প্রফেশনাল হেডার যাতে সাইট ব্লক না করে
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ArchitectX-DeepClone/2.0',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        
        ux_spinner.update("Bypassing firewalls and downloading DOM structure...", "cyan")
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        ux_spinner.update("Extracting UI/UX patterns and Color Schemes...", "magenta")
        
        # কালার স্কিম এক্সট্র্যাক্ট
        color_palette = extract_colors(html_content)
        
        # অপ্রয়োজনীয় ট্যাগ বাদ দেওয়া
        for script in soup(["script", "style", "noscript", "meta", "svg"]):
            script.extract()
            
        # কোর ডেটা এক্সট্র্যাক্ট
        title = soup.title.string.strip() if soup.title else "Unknown Title"
        
        # ন্যাভিগেশন এবং বাটন স্ট্রাকচার
        nav_links = [a.get_text(strip=True) for a in soup.find_all('a') if len(a.get_text(strip=True)) > 2][:5]
        buttons = [b.get_text(strip=True) for b in soup.find_all(['button', 'a']) if 'btn' in b.get('class', []) or 'button' in b.get('class', [])][:5]
        
        # লেআউট স্ট্রাকচার
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2']) if h.get_text(strip=True)][:4]
        
        ux_spinner.stop("Target DNA successfully sequenced!")
        
        # AI-এর জন্য মাস্টার ব্লুপ্রিন্ট তৈরি
        blueprint = f"""
        CLONE TARGET DATA:
        - Original Title: {title}
        - Discovered Color Palette: {', '.join(color_palette) if color_palette else 'Use modern tech dark theme'}
        - Navigation Menu Items: {', '.join(nav_links)}
        - Core Call-to-Actions (Buttons): {', '.join(buttons)}
        - Main Structural Headings: {', '.join(headings)}
        
        INSTRUCTION: Act as ArchitectX Clone Engine. Rebuild this exact website structure. 
        Use the discovered color palette. Ensure the UI feels identical but uses clean, modern HTML5/CSS3.
        """
        return blueprint

    except requests.exceptions.MissingSchema:
        ux_spinner.stop("Invalid URL. Provide complete format (e.g., https://example.com)", success=False)
        return None
    except requests.exceptions.RequestException as e:
        ux_spinner.stop(f"Target is heavily protected or offline. Error: {e}", success=False)
        return None
    except Exception as e:
        ux_spinner.stop(f"Deep-Clone engine failure: {e}", success=False)
        return None
