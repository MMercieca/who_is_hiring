from analyzers import ask_ai

def find_careers_page(links):
    if not links:
        return None

    prompt = f"""
    You are a research assistant that identifies careers pages.  Search the links
    to identify which link is the careers page.

    Be careful.  

    Prioritize links that match these terms:
    1. "Apply Now" or "Search Jobs"
    2. "Openings" or "Vacancies"
    3. "Join our Team" or "Work with us"
    4. "Careers" or "Jobs"
    
    Return ONLY the URL of the careers page. Do not explain. If it is not found, return "None".

    Input Links:
    {links}
    """


    return ask_ai.query(prompt)