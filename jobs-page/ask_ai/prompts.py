def find_company(target_company):
  return f"""
    You are a corporate research assistant.  Search the web to find the official company website
    of the company listed below.

    Be careful.  Find the company website, not reviews or ads.  

    Return ONLY the URL of the company website. Do not explain. If it is not found, return "None".

    Company:
    {target_company}
    """

def find_job_page(links):
  return f"""
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
    {links}
    """
  
