import requests
from bs4 import BeautifulSoup
from rich.console import Console

console = Console()

def scrape_website(url):
    """
    ইউজারের দেওয়া লিংকে গিয়ে ওয়েবসাইটের ডিজাইন, লেআউট এবং কন্টেন্ট স্ক্যান করে।
    """
    console.print(f"\n[bold yellow][*] ArchitectX Web Scraper initializing for URL...[/bold yellow]")
    console.print(f"[cyan]Target: {url}[/cyan]")
    
    try:
        # প্রফেশনাল ব্রাউজারের মতো রিকোয়েস্ট পাঠানোর জন্য হেডার
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 ArchitectX/1.0'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        console.print("[yellow][*] Extracting DOM structure and layout patterns...[/yellow]")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # স্ক্রিপ্ট এবং স্টাইল ট্যাগগুলো বাদ দিচ্ছি যাতে শুধু মূল স্ট্রাকচার পাই
        for script in soup(["script", "style", "noscript"]):
            script.extract()
            
        # ওয়েবসাইটের মূল তথ্যগুলো বের করে আনা
        title = soup.title.string if soup.title else "Unknown Title"
        
        # হেডিং এবং প্যারাগ্রাফ এক্সট্র্যাক্ট করা (ডিজাইনের লেআউট বোঝার জন্য)
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3']) if h.get_text(strip=True)]
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]
        
        # বাটনের টেক্সট এবং লিংক স্ট্রাকচার (UI/UX বোঝার জন্য)
        buttons = [b.get_text(strip=True) for b in soup.find_all(['button', 'a']) if b.get_text(strip=True) and len(b.get_text(strip=True)) < 20]

        console.print("[bold green][✔] Website DNA successfully extracted![/bold green]")
        
        # AI-এর জন্য একটি কাস্টম প্রম্পট বা ব্লুপ্রিন্ট তৈরি করা
        extracted_blueprint = f"""
        I need to clone the design and layout of a website. Here is its extracted data:
        - Target Website Title: {title}
        - Main Headings (Use these for structural hierarchy): {', '.join(headings[:5])}
        - Content Vibe (Use similar placeholder texts): {' '.join(paragraphs[:3])}
        - Call to Actions (Buttons): {', '.join(buttons[:5])}
        
        INSTRUCTION: Create a highly responsive, modern website using HTML, CSS, and JS that perfectly mimics the layout, UI/UX, and structure of this extracted data. Make it look professional and ready to deploy.
        """
        return extracted_blueprint

    except requests.exceptions.MissingSchema:
        console.print("[bold red][!] Invalid URL format. Please include http:// or https://[/bold red]")
        return None
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red][!] Scraper Error: Could not access the website. It might be protected or offline.[/bold red]")
        return None
    except Exception as e:
        console.print(f"[bold red][!] Unknown Scraper Error: {e}[/bold red]")
        return None

# টেস্ট করার জন্য
if __name__ == "__main__":
    test_url = "https://example.com"
    blueprint = scrape_website(test_url)
    if blueprint:
        print("\nGenerated AI Blueprint:", blueprint)
