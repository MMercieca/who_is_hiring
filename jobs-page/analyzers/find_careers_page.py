from openai import OpenAI
import json
import config
import re

def find_careers_page(links):
    if not links:
        return None

    links_str = json.dumps(links, indent=2)
    
    prompt = f"""
    You are a helpful assistant that identifies job pages.  Search the web
    to find the page that lists the open positions for the target company.

    Be careful.  Be sure to search the official company website.  Return the page
    that lists all of the open positions.  Return ONLY the URL for that page.
    
    Return ONLY the URL. Do not explain. If none are relevant, return "None".

    Links:
    {links_str}
    """

    try:
        openai = OpenAI(api_key=config.OPENAI_KEY)
        response = openai.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.choices[0].message.content
        
        url_match = re.search(r'https?://[^\s"\'\`<>]+', content)
        
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
        print(f"Info --- LLM Error: {e}")
        return None