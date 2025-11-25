import config
import requests

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
        print(f"Info --- Search API Error: {e}")
        return None

def google_career_page(target_company, website=""):
  if website != None and len(website) > 0:
    results = run_query(f"careers page site:{website}")
  else:
    results = run_query(f"careers page for \"{target_company}\"")

  if results and 'items' in results:
      return results['items'][0]['link']
  return None