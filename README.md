# 📄 Basic Wikipedia Corpus Scraper

This project is a simple, effective tool for extracting the main article text from any given Wikipedia URL. It uses **Streamlit** for an interactive web interface and basic **BeautifulSoup** parsing to clean the article content.

The main goal is to generate a clean text corpus, free from typical web elements and reference links, ready for analysis or use in other projects.

## ✨ Key Features

* **URL Input:** Accepts a full Wikipedia article URL (e.g., `https://en.wikipedia.org/wiki/Python_(programming_language)`).
* **Simple Fetching:** Uses the `requests` library to fetch the page content.
* **Text Cleaning:** Parses the HTML using `BeautifulSoup` to isolate paragraph content.
* **Reference Removal:** Cleans the text by removing bracketed reference markers (e.g., `[1]`, `[15]`).
* **Error Handling:** Includes basic error handling for failed requests or bad URLs.
* **Display:** Presents the cleaned text corpus directly in the Streamlit UI.

## 💻 Tech Stack

* **Frontend/UI:** [Streamlit](https://streamlit.io/)
* **Scraping:** [Requests](https://pypi.org/project/requests/)
* **HTML Parsing:** [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
