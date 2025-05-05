# import re
# from bs4 import BeautifulSoup
# from playwright.sync_api import sync_playwright, TimeoutError

# def scrape_url(url, timeout=60000, wait_strategy="domcontentloaded"):
#     """
#     Scrape content from a JS-rendered page using Playwright.
    
#     Args:
#         url (str): The URL to scrape
#         timeout (int): Timeout in milliseconds (default: 60000 - 60 seconds)
#         wait_strategy (str): Page load strategy - options:
#             - "domcontentloaded": Faster, waits for DOM to load
#             - "load": Waits for all resources
           
    
#     Returns:
#         str: Scraped and cleaned text content
#     """
#     try:
#         with sync_playwright() as p:
#             browser = p.chromium.launch(headless=True)
#             context = browser.new_context(
#                 user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#             )
#             page = context.new_page()
            
        
#             try:
#                 page.goto(url, wait_until=wait_strategy, timeout=timeout)
#             except TimeoutError:
#                 print(f"Warning: Initial timeout with {wait_strategy}, continuing anyway...")
                
            
#             if wait_strategy != "networkidle":
#                 page.wait_for_timeout(2000)  # 2 second delay
                
#             html = page.content()
#             browser.close()
        
        
#         soup = BeautifulSoup(html, 'html.parser')
        
#         for tag in soup(["script", "style", "nav", "header", "footer", "iframe", "noscript", "aside"]):
#             tag.decompose()

#         text = soup.get_text(separator=' ')
#         text = re.sub(r'\n+', '\n', text)
#         text = re.sub(r'\s+', ' ', text)
        
#         return text.strip()
    
#     except Exception as e:
#         return f"Error scraping {url}: {str(e)}"


import re
import requests

from bs4 import BeautifulSoup


def scrape_url( url):
    """Scrape content from a URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script, style elements and navigation/header/footer if possible
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.decompose()
        
        # Get text and clean it
        text = soup.get_text()
        # Remove excessive newlines and whitespace
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"