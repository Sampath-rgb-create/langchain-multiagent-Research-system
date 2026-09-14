from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from rich import print
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re


load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
@tool
def web_search(query: str) -> str:
    """
    Perform a web search using the Tavily API.

    Args:
        query (str): The search query.

    Returns:
        str: The search results.
    """

    results = tavily.search(query=query,max_results=2)

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"

        )

    return "\n----\n".join(out)


@tool
def scrape_url(url):
    """
    Fetches a URL and extracts the page title and all text content.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers, timeout=10)
        
        # Raise an exception for bad status codes (404, 500, etc.)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Clean up the soup by removing scripts and styles
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
            
        # Extract basic information
        data = {
            "title": soup.title.string.strip() if soup.title else "No Title",
            "text": " ".join(soup.get_text().split())
        }
        return data

    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to retrieve data: {e}"}

# Example usage:
# print(scrape_url("https://example.com"))







    