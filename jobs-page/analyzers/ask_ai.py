# ask_ai.py

from openai import OpenAI
import config
import re

def query(prompt):
  try:
    openai = OpenAI(api_key=config.OPENAI_KEY)
    response = openai.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content

    url_match = re.search(r'https?://[^\s"\'\`<>]+', content)

    if url_match:
        return url_match.group(0)

    # 2. Fallback: If you have relative links (e.g., /jobs), look for those
    # (Only needed if your scraper didn't convert them to absolute URLs earlier)
    relative_match = re.search(r'/[a-zA-Z0-9/_.-]+', content)
    if relative_match:
        return relative_match.group(0)
        
    # If regex finds nothing, try a basic clean as a last resort
    return content.strip().strip('"').strip("'").strip("`").strip("`")
      
  except Exception as e:
      print(f"Info --- LLM Error: {e}")
      return None
  