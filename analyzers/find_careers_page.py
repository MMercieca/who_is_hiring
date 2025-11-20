import ollama
import json
import config

def find_careers_page(links):
    if not links:
        return None

    links_str = json.dumps(links, indent=2)
    
    prompt = f"""
    You are a helpful assistant that identifies job pages.
    Below is a list of links from a company website.
    Identify the ONE link that most likely leads to a list of open job positions.
    Look for terms like "Careers", "Jobs", "Join Us", "Openings", or "Work with us".
    
    Return ONLY the URL. Do not explain. If none are relevant, return "None".

    Links:
    {links_str}
    """

    try:
        response = ollama.chat(model=config.OLLAMA_MODEL, messages=[
            {'role': 'user', 'content': prompt},
        ])
        
        best_link = response['message']['content'].strip().strip('"').strip("'").strip("`")
        return best_link

    except Exception as e:
        print(f"Ollama Error: {e}")
        return None