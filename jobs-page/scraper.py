import requests
from bs4 import BeautifulSoup

def get_html_content(url):
    headers = {
        "User-Agent": "Lynx/2.8.7rel.2 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/1.0.0a"
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
        
        # Basic cleanup
        if text and href and not href.startswith(('javascript', '#', 'mailto')):
            if href.startswith('/'):
                href = base_url.rstrip('/') + href
            
            # Create the link object
            link_obj = {"text": text, "url": href}
            
            # --- SCORE THE LINK ---
            # specific keywords get a high score (0 = highest priority)
            lower_text = text.lower()
            lower_href = href.lower()
            
            priority = 2 # Default priority (lowest)
            
            # Priority 0: High confidence keywords
            if any(x in lower_text for x in ['career', 'job', 'opening', 'join us', 'apply', 'apply now', 'work with']):
                priority = 0
            elif any(x in lower_href for x in ['career', 'job', 'opening', 'apply']): # distinct from text
                priority = 0
                
            # Priority 1: Weaker keywords
            elif any(x in lower_text for x in ['about', 'team', 'company']):
                priority = 1

            # Store with priority for sorting
            links.append((priority, link_obj))
            
    # Sort by priority (0 first, then 1, then 2)
    links.sort(key=lambda x: x[0])
    
    # Extract just the link objects and take the top 100
    sorted_links = [x[1] for x in links]
    
    return sorted_links[:100]