import config

def google_enabled():
  return len(config.GOOGLE_API_KEY) > 0 and len(config.GOOGLE_CX_ID) > 0
