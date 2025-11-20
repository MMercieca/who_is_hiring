import requests
import config # Import the file we just made above

def run_query(query):
    url = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        'key': config.GOOGLE_API_KEY,
        'cx': config.GOOGLE_CX_ID,
        'q': query,
        'num': 1 
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Good practice to catch 403/404 errors
        results = response.json()

        if 'items' in results:
            return results
        else:
            return None
    except Exception as e:
        print(f"Search API Error: {e}")
        return None

def find_company_website(company_name):
    print(f"Searching Google for {company_name}...")
    results = run_query(f"{company_name} official website")
    if results:
        return results['items'][0]['link']
    return None

def find_initial_career_page(website):
    print(f"Searching Google for career page on {website}...")
    results = run_query(f"open positions site:{website}")
    if results and 'items' in results:
        return results['items'][0]['link']
    return None