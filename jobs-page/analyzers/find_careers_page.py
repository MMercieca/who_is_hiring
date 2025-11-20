import ollama
import json
import config
import re

def find_careers_page(links):
    if not links:
        return None

    links_str = json.dumps(links, indent=2)
    
    prompt = f"""
    You are a helpful assistant that identifies job pages.
    Below is a list of links from a company website.
    Identify the ONE link that most likely leads to a list of open job positions.
    
    Prioritize links that match these terms:
    1. "Apply Now" or "Search Jobs"
    2. "Openings" or "Vacancies"
    3. "Join our Team" or "Work with us"
    4. "Careers" or "Jobs"
    
    Return ONLY the URL. Do not explain. If none are relevant, return "None".

    Links:
    {links_str}
    """

    try:
        response = ollama.chat(model=config.OLLAMA_MODEL, messages=[
            {'role': 'user', 'content': prompt},
        ])
        
        content = response['message']['content']
        
        url_match = re.search(r'https?://[^\s"<>]+', content)
        
        if url_match:
            return url_match.group(0)
        
        # 2. Fallback: If you have relative links (e.g., /jobs), look for those
        # (Only needed if your scraper didn't convert them to absolute URLs earlier)
        relative_match = re.search(r'/[a-zA-Z0-9/_.-]+', content)
        if relative_match:
            return relative_match.group(0)
            
        # If regex finds nothing, try a basic clean as a last resort
        return content.strip().strip('"').strip("'").strip("`").strip("`")
        
    except Exception as e:
        print(f"Ollama Error: {e}")
        return None