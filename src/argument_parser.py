# src/argument_parser.py
import argparse
import logging

from src.search import search_for_term
from src.interaction import like_tweet, comment_on_tweet, retweet_tweet, quote_tweet
from src.user import TwitterUser
from src.scraper import TwitterScraper
from src.summarizer import summarize_scraped_data
from src import utils

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Selenium Twitter Automation - Automate Twitter interactions"
    )

    # General user authentication arguments
    parser.add_argument(
        "-e", "--email", type=str, required=True, help="Your Twitter account email"
    )
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        required=True,
        help="Your Twitter account password",
    )

    # Actions for different interactions
    parser.add_argument(
        "-s",
        "--search",
        type=str,
        help="Search Twitter for a specific term or hashtag (e.g., 'selenium')",
    )
    parser.add_argument(
        "-lk", "--like", type=str, help="Like a specific tweet by tweet ID"
    )
    parser.add_argument(
        "-twt", "--tweet", type=str, help="Post a tweet with the given content"
    )
    parser.add_argument(
        "-com", "--comment", type=str, help="Comment on a specific tweet by tweet ID"
    )
    parser.add_argument(
        "-ret", "--retweet", type=str, help="Retweet a tweet by tweet ID"
    )
    parser.add_argument("-quo", "--quote", type=str, help="Quote a tweet by tweet ID")
    parser.add_argument("-fol", "--follow", type=str, help="Follow a user by username")
    parser.add_argument(
        "-unf", "--unfollow", type=str, help="Unfollow a user by username"
    )
    parser.add_argument(
        "-pr", "--profile", action="store_true", help="Open your profile page"
    )
    parser.add_argument(
        "-out", "--output", type=str, help="Output file for results (CSV, JSON, etc.)"
    )

    # Summarize scraped tweets
    parser.add_argument(
        "-sum", "--summarize", action="store_true", help="Summarize scraped tweets"
    )

    # Parse arguments
    args = parser.parse_args()

    # Handle actions
    handle_actions(args)

    return args


def handle_actions(args):
    """
    Handles each action based on the arguments.
    We create a single scraper instance if needed, and close it after the actions.
    """
    scraper = None
    user_actions = None

    # Because search, follow, tweet, etc., require login, create the scraper and log in once if needed
    if any(
        [
            args.search,
            args.like,
            args.comment,
            args.retweet,
            args.quote,
            args.follow,
            args.unfollow,
            args.profile,
            args.tweet,
        ]
    ):

        # Initialize the scraper and log in
        scraper = TwitterScraper(email=args.email, password=args.password)
        scraper.login()
        user_actions = TwitterUser(scraper.driver, scraper.actions)

    # 1. SEARCH
    if args.search:
        logging.info(f"Searching for: {args.search}")
        search_for_term(scraper, args.search)

    # 2. LIKE
    if args.like:
        logging.info(f"Liking tweet with ID: {args.like}")
        like_tweet(scraper.driver, tweet_id=args.like)

    # 3. TWEET
    if args.tweet:
        logging.info(f"Posting tweet: {args.tweet}")
        user_actions.create_new_tweet(args.tweet)

    # 4. COMMENT
    if args.comment:
        logging.info(f"Commenting on tweet with ID: {args.comment}")
        comment_on_tweet(
            scraper.driver,
            scraper.actions,
            tweet_id=args.comment,
            text="This is a comment!",
        )

    # 5. RETWEET
    if args.retweet:
        logging.info(f"Retweeting tweet with ID: {args.retweet}")
        retweet_tweet(scraper.driver, tweet_id=args.retweet)

    # 6. QUOTE
    if args.quote:
        logging.info(f"Quoting tweet with ID: {args.quote}")
        quote_tweet(scraper.driver, tweet_id=args.quote, quote_text="My thoughts...")

    # 7. FOLLOW
    if args.follow:
        logging.info(f"Following user: {args.follow}")
        user_actions.follow_user(args.follow)

    # 8. UNFOLLOW
    if args.unfollow:
        logging.info(f"Unfollowing user: {args.unfollow}")
        user_actions.unfollow_user(args.unfollow)

    # 9. PROFILE
    if args.profile:
        logging.info("Opening user profile page...")
        user_actions.open_profile_page()

    # Summarize any scraped tweets so far
    if args.summarize and scraper:
        summarize_scraped_data(scraper.data)

    # 10. OUTPUT
    if args.output and scraper and scraper.data:
        logging.info(f"Saving output to: {args.output}")
        scraper.save_data(output_file=args.output)

    # Quit the driver if it was created
    if scraper:
        scraper.driver.quit()
        logging.info("WebDriver closed.")
