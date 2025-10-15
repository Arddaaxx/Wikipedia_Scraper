# wikipedia_scraper.py
# Make sure this file is in the same folder as streamlit_app.py or is installable.

import requests
from bs4 import BeautifulSoup
import re

DEFAULT_USER_AGENT = "(contact: aryaamin233@gmail.com)"

class WikipediaScrapeError(Exception):
    pass

def scrape_wikipedia(title: str, user_agent: str = DEFAULT_USER_AGENT, timeout: int = 15):
    """
    Given a title string, find the best wikipedia page and return (filename, corpus_text).
    Raises WikipediaScrapeError on failure.
    """
    title_clean = title.strip()
    if not title_clean:
        raise WikipediaScrapeError("Empty title provided.")

    # 1) use opensearch to find matching page
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": title_clean,
        "limit": 1,
        "namespace": 0,
        "format": "json"
    }

    try:
        res = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    except Exception as e:
        raise WikipediaScrapeError(f"Failed to query Wikipedia API: {e}")

    if res.status_code != 200:
        raise WikipediaScrapeError(f"Wikipedia API returned status {res.status_code}")

    try:
        data = res.json()
    except Exception as e:
        raise WikipediaScrapeError(f"Failed to parse JSON response from Wikipedia API: {e}")

    if not data or len(data) < 4 or not data[3]:
        raise WikipediaScrapeError("No page found for this search query.")

    wiki_link = data[3][0]

    # 2) fetch the article page
    headers = {"User-Agent": user_agent or DEFAULT_USER_AGENT}
    try:
        response = requests.get(wiki_link, headers=headers, timeout=timeout)
    except Exception as e:
        raise WikipediaScrapeError(f"Failed to fetch Wikipedia page: {e}")

    if response.status_code != 200:
        raise WikipediaScrapeError(f"Failed to fetch article: HTTP {response.status_code}")

    soup = BeautifulSoup(response.content, "html.parser")

    # Gather <p> text, skipping empty strings and edit links
    paragraphs = [p.get_text(separator=" ", strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]
    corpus = "\n\n".join(paragraphs).strip()

    # remove reference markers like [1], [2], or [12]
    corpus = re.sub(r"\[\d+\]", "", corpus)

    # safe filename: replace problematic chars
    safe_title = re.sub(r"[\\/*?\"<>|:]", "_", title_clean)
    filename = f"{safe_title}.txt"

    return filename, corpus
