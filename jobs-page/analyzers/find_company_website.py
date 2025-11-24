from analyzers import ask_ai

def find_company_website(target_company):
    if not target_company:
        return None

    prompt = f"""
    You are a corporate research assistant.  Search the web to find the official company website
    of the company listed below.

    Be careful.  Find the company website, not reviews or ads.  

    Return ONLY the URL of the company website. Do not explain. If it is not found, return "None".

    Company:
    {target_company}
    """

    return ask_ai.query(prompt)