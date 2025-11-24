from analyzers import ask_ai

def find_job_listings(links, start_page):
    if not links:
        return None

    prompt = f"""
    You are a research assistant that identifies careers pages.  Search the links
    to identify which link lists all of the open positions for the company.

    Be careful.  This page is likely different from the career starting page of {start_page}

    Prioritize links that match these terms:
    1. "Apply Now" or "Search Jobs"
    2. "View openings"
    3. "See all openings"
    4. "Join our team"
    
    Return ONLY the URL of the careers page. Do not explain. If it is not found, return "None".

    Input Links:
    {links}
    """


    return ask_ai.query(prompt)