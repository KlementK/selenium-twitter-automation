# src/search.py
import logging
from src.scraper import TwitterScraper


def search_for_term(scraper: TwitterScraper, term: str):
    """
    Uses the existing `scraper` to search for a term or hashtag,
    scraping some tweets in the process.
    """
    logging.info(f"Performing search for term: {term}")
    if term.startswith("#"):
        # hashtag
        scraper.scrape_tweets(scrape_hashtag=term)
    else:
        # general query
        scraper.scrape_tweets(scrape_query=term)
