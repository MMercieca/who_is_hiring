import requests
from bs4 import BeautifulSoup

def get_html_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as err:
        print(f"Download Error: {err}")
        return None

def extract_links(html, base_url):
    if not html:
        return []
        
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    
    for tag in soup.find_all('a', href=True):
        text = tag.get_text(strip=True)
        href = tag['href']
        
        if text and href and not href.startswith(('javascript', '#', 'mailto')):
            # Handle relative links (e.g., "/jobs" -> "https://site.com/jobs")
            if href.startswith('/'):
                href = base_url.rstrip('/') + href
            links.append({"text": text, "url": href})
            
    return links[:100]