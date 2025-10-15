# streamlit_app.py
import streamlit as st
from wikipedia_scraper import scrape_wikipedia, WikipediaScrapeError
import time

st.set_page_config(page_title="Wikipedia Scraper", layout="centered")

st.title("📚 WikiCorpus Builder (Modern Scraper")
st.caption("Scrape, Clean, and Analyze Wikipedia Articles")
st.markdown("Type a topic, press *Scrape*, preview the article, and download a `.txt` file.")

title_input = st.text_input("Search title", placeholder="e.g. Albert Einstein")

col1, col2 = st.columns([1,1])
with col1:
    scrape_btn = st.button("Scrape")
with col2:
    clear_btn = st.button("Clear")

if clear_btn:
    st.experimental_rerun()

if scrape_btn:
    if not title_input.strip():
        st.warning("Please enter a title to search.")
    else:
        with st.spinner("Searching Wikipedia..."):
            try:
                filename, corpus = scrape_wikipedia(title_input)
            except WikipediaScrapeError as e:
                st.error(f"Error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
            else:
                if not corpus:
                    st.info("No textual content found on that page.")
                else:
                    st.success(f"Scraped: {filename}")
                    # Show approx size and first 20 lines
                    st.markdown(f"**Character length:** {len(corpus):,}")
                    st.download_button(
                        label="Download as .txt",
                        data=corpus,
                        file_name=filename,
                        mime="text/plain"
                    )
                    st.markdown("---")
                    st.subheader("Preview (first 5000 characters)")
                    st.code(corpus[:5000], language="text")
                    if len(corpus) > 5000:
                        if st.button("Show more"):
                            st.code(corpus[5000:15000], language="text")
