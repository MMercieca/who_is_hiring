# analyzers/job_extractor.py
import ollama
import json
import config

def extract_jobs_from_links(links):
    """
    Takes a list of link dictionaries: [{'text': '...', 'url': '...'}, ...]
    Returns a list of found jobs: [{'title': '...', 'url': '...'}]
    """
    if not links:
        return []

    found_jobs = []
    
    # We process links in chunks of 50 to avoid overwhelming the context window
    chunk_size = 50
    
    print(f"Analyzing {len(links)} links to find specific job openings...")

    for i in range(0, len(links), chunk_size):
        chunk = links[i:i + chunk_size]
        links_json = json.dumps(chunk)

        prompt = f"""
        You are a data extraction assistant.
        Below is a JSON list of links found on a company career page.
        Your goal is to extract ONLY the links that represent specific job openings.

        Rules:
        1. Look for specific roles (e.g., "Software Engineer", "Account Manager").
        2. IGNORE general navigation links (e.g., "Home", "Benefits", "Login", "Next Page", "Read More").
        3. IGNORE filters or categories (e.g., "Engineering Department", "Remote Locations").
        
        Return a JSON list of objects with keys: "title" and "url".
        If no jobs are found in this batch, return an empty list [].
        Do not output markdown. Return ONLY raw JSON.

        Input Links:
        {links_json}
        """

        try:
            response = ollama.chat(model=config.OLLAMA_MODEL, messages=[
                {'role': 'user', 'content': prompt},
            ])
            
            content = response['message']['content']
            
            # Clean up common LLM mistakes (Markdown code blocks)
            content = content.replace("```json", "").replace("```", "").strip()
            
            # Parse JSON
            batch_jobs = json.loads(content)
            
            if isinstance(batch_jobs, list):
                found_jobs.extend(batch_jobs)
                
        except json.JSONDecodeError:
            print("Warning: AI returned invalid JSON. Skipping this batch.")
        except Exception as e:
            print(f"Error in job extraction: {e}")

    # Remove duplicates based on URL
    unique_jobs = {v['url']: v for v in found_jobs}.values()
    return list(unique_jobs)