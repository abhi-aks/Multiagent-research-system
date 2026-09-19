from langchain.tools import tool
from exa_py import Exa
import os
from dotenv import load_dotenv
from rich import print
import requests
from bs4 import BeautifulSoup

load_dotenv()

exa = Exa(api_key=os.getenv("EXA_API_KEY"))

NUM_RESULTS = 5


@tool
def web_search(query: str) -> str:
    """Search the web and return 5 relevant sources with titles and URLs."""

    results = exa.search(
        query=query,
        num_results=NUM_RESULTS
    )

    out = [] #to save the result in 

    for r in results.results:
        out.append(
            f"Title: {r.title}\n"
            f"URL: {r.url}"
        )

    return "\n\n----\n\n".join(out)


# print(web_search.invoke("What are the possible outcome if FED increases rate?"))

@tool
def scrape_url(url:str)->str:
    """Scrap and return clean content from given URLs"""
    try: 
        resp = requests.get(url,timeout=8,headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(resp.text,"html.parser")
        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator=" ",strip='True')[:3000]
    except Exception as e:
        return f"Could not scrape URL:{str(e)}"
#(scrape_url.invoke())