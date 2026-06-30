from tavily import TavilyClient

import os
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def tavily_search(query):
    response = client.search(
        query=query,
        max_results=5
    )
    
    
    result = []
    for i,r in enumerate(response["results"]):
        title = r.get("title","unknown")
        snippet = r.get("content","").strip()
        urls = r.get("url","")
        
        if len(snippet)>300:
            snippet = snippet[:300].rsplit(" ",1)[0]+"..."
        result.append(f"{i}.**{title}\n  {urls}\n  {snippet}")
        
    return "\n\n".join(result)



