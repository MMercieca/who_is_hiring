import requests
from bs4 import BeautifulSoup
import ollama
import json



def find_company_website(company_name):
  results = run_query(f"{company_name} official website")
  if results:
    return results['items'][0]['link']
  else:
     None

def get_html_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # 2. Make the GET request
        response = requests.get(url, headers=headers, timeout=10)
        
        # 3. Check if the request was successful (Status Code 200)
        response.raise_for_status()
        
        # 4. Return the HTML text
        return response.text

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except requests.exceptions.ConnectionError as err:
        print(f"Connection Error: {err}")
    except requests.exceptions.Timeout as err:
        print(f"Timeout Error: {err}")
        
    return None

def open_positions(website):
   results = run_query(f"open positions site:{website}")
   if 'items' in results:
      return results['items'][0]['link']
   else:
      return None


def run_query(query):
    url = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        'key': API_KEY,
        'cx': API_CX,
        'q': query,
        'num': 1 # We only want the top result
    }
    
    try:
      response = requests.get(url, params=params)
      results = response.json()

      if 'items' in results:
          return results
      else:
          return None
    except Exception as e:
        print("{e}")

def get_links(html, url):
  soup = BeautifulSoup(html, 'html.parser')
        
  links = []
  # Find all 'a' tags with an href attribute
  for tag in soup.find_all('a', href=True):
      text = tag.get_text(strip=True)
      href = tag['href']
      
      # Filter out empty links or javascript triggers
      if text and href and not href.startswith(('javascript', '#', 'mailto')):
          # Clean up relative URLs (e.g., "/jobs" -> "https://site.com/jobs")
          if href.startswith('/'):
              href = url.rstrip('/') + href
          links.append({"text": text, "url": href})
          
  return links[:100] # Limit to first 100 links to save tokens

def find_jobs_link_with_ollama(links):
    """
    Sends the list of links to Ollama to decide which one is the careers page.
    """
    if not links:
        return None

    # prepare the prompt
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
        response = ollama.chat(model='phi4:latest', messages=[
            {'role': 'user', 'content': prompt},
        ])
        
        # Clean the response (sometimes LLMs add quotes or whitespace)
        best_link = response['message']['content'].strip().strip('"').strip("'")
        return best_link

    except Exception as e:
        print(f"Ollama Error: {e}")
        return None

website = find_company_website("TechSmith")
print("Company website:", website)
print("...")
print(f"Searching {website} for jobs page")

jobs_page = open_positions(website)
print("Trying ", jobs_page)

content = get_html_content(jobs_page)

links = get_links(content, website)
link = find_jobs_link_with_ollama(links)
print("Trying: ", link)




