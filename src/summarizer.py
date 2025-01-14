# src/summarizer.py
import logging


def summarize_scraped_data(tweet_dicts):
    """
    Very basic placeholder for summarizing tweets.
    Expects a list of tweet dictionaries (with 'content' key).
    """
    if not tweet_dicts:
        logging.info("No tweets to summarize.")
        return

    # Naive approach: just combine contents & truncate for "summary"
    combined_text = " ".join(t.get("content", "") for t in tweet_dicts)
    summary = combined_text[:200] + "..." if len(combined_text) > 200 else combined_text

    logging.info("----- TWEET SUMMARY START -----")
    logging.info(summary)
    logging.info("----- TWEET SUMMARY END -----")

    return summary
