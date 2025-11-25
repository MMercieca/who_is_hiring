from ask_ai import query

def find_company_website(target_company):
    if not target_company:
        return None

    prompt = f"""
    You are a corporate research assistant.  Search the web to find the official company website
    of the company listed below.

    Some guidelines to identify the company website:

    1. If the company name has a strange spelling, the website may be the company name followed by `.com`
    2. If the company name has a normal spelling, the website may the company name with no spaces followed by a `.com`
    3. If the company name is long some words of the name may be omitted.
    4. Sometimes spaces are replaced with dashes.
    
    Return ONLY the URL of the company website. Do not explain. If it is not found, return "None".

    Company:
    {target_company}
    """

    return query(prompt)