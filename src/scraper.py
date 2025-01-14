# src/scraper.py
import logging
import sys
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
)
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains

from src.scroller import Scroller
from src.tweet import Tweet
from src import utils

TWITTER_LOGIN_URL = "https://twitter.com/i/flow/login"


class TwitterScraper:
    """
    Main class for logging into Twitter and (optionally) scraping tweets.
    """

    def __init__(self, email=None, password=None, max_tweets=50, headless=False):
        logging.info("Initializing TwitterScraper...")
        self.email = email
        self.password = password
        self.max_tweets = max_tweets
        self.interrupted = False
        self.tweet_ids = set()
        self.data = []  # Store scraped tweet dictionaries

        # Initialize driver
        self.driver = self._get_driver(headless)
        self.actions = ActionChains(self.driver)
        self.scroller = Scroller(self.driver)

    def _get_driver(self, headless=False):
        """
        Set up and return the Selenium WebDriver (Firefox) using Selenium 4 syntax.
        """
        logging.info("Setting up WebDriver with Firefox...")
        options = FirefoxOptions()

        if headless:
            options.add_argument("--headless")

        # Import the Service class here
        from selenium.webdriver.firefox.service import Service

        # Provide the path to your geckodriver.exe
        service = Service("webdriver/geckodriver.exe")

        try:
            # Note: 'executable_path' is deprecated; use the Service object instead.
            driver = webdriver.Firefox(service=service, options=options)
            logging.info("WebDriver Setup Complete.")
            return driver
        except WebDriverException as e:
            logging.error(f"Error setting up WebDriver: {e}", exc_info=True)
            sys.exit(1)

    def login(self):
        """
        Log into Twitter using the provided email & password.
        """
        if not self.email or not self.password:
            raise ValueError("Email and password must be provided for login.")

        logging.info("Logging into Twitter...")
        try:
            self.driver.maximize_window()
            self.driver.get(TWITTER_LOGIN_URL)
            sleep(3)

            self._input_username()
            self._handle_unusual_activity()
            self._input_password()

            cookies = self.driver.get_cookies()
            auth_token = next(
                (
                    cookie["value"]
                    for cookie in cookies
                    if cookie["name"] == "auth_token"
                ),
                None,
            )
            if not auth_token:
                raise ValueError("Login failed: Could not find auth_token cookie.")

            logging.info("Login successful.")

        except Exception as e:
            logging.error(f"Login Failed: {e}", exc_info=True)
            sys.exit(1)

    def _input_username(self):
        for attempt in range(3):
            try:
                username_field = self.driver.find_element(
                    "xpath", "//input[@autocomplete='username']"
                )
                username_field.send_keys(self.email)
                username_field.send_keys(Keys.RETURN)
                sleep(3)
                return
            except NoSuchElementException:
                logging.warning(f"Failed to find username field, attempt {attempt+1}")
                sleep(2)
        raise NoSuchElementException("Failed to input username after 3 attempts.")

    def _handle_unusual_activity(self):
        """
        Handle second prompt if Twitter demands additional confirmation.
        """
        try:
            unusual_activity_field = self.driver.find_element(
                "xpath", "//input[@data-testid='ocfEnterTextTextInput']"
            )
            unusual_activity_field.send_keys(self.email)
            unusual_activity_field.send_keys(Keys.RETURN)
            sleep(3)
        except NoSuchElementException:
            pass  # No prompt

    def _input_password(self):
        for attempt in range(3):
            try:
                password_field = self.driver.find_element(
                    "xpath", "//input[@autocomplete='current-password']"
                )
                password_field.send_keys(self.password)
                password_field.send_keys(Keys.RETURN)
                sleep(3)
                return
            except NoSuchElementException:
                logging.warning(f"Password field not found, attempt {attempt+1}")
                sleep(2)
        raise NoSuchElementException("Failed to input password after 3 attempts.")

    def scrape_tweets(
        self,
        max_tweets=50,
        scrape_username=None,
        scrape_hashtag=None,
        scrape_query=None,
        scrape_latest=True,
        scrape_top=False,
        scrape_poster_details=False,
        no_tweets_limit=False,
    ):
        """
        General scraping logic for home, profile, hashtag, or search query.
        """
        self.max_tweets = max_tweets
        self.data = []
        self.tweet_ids = set()

        # Navigate
        if scrape_username:
            self._go_to_profile(scrape_username)
        elif scrape_hashtag:
            self._go_to_hashtag(scrape_hashtag, scrape_latest, scrape_top)
        elif scrape_query:
            self._go_to_search(scrape_query, scrape_latest, scrape_top)
        else:
            self._go_to_home()

        logging.info("Starting tweet scraping...")

        # Try to dismiss cookies
        self._dismiss_cookies_banner()

        # Main scraping loop
        while self.scroller.scrolling:
            try:
                self._collect_tweets(scrape_poster_details, no_tweets_limit)
                # If we reached our max, or no_tweets_limit is True, stop
                if len(self.data) >= max_tweets and not no_tweets_limit:
                    break
            except KeyboardInterrupt:
                logging.info("Scraping interrupted by user.")
                self.interrupted = True
                break
            except Exception as e:
                logging.error(f"Error while scraping: {e}", exc_info=True)
                break

        logging.info(f"Scraping complete. Collected {len(self.data)} tweets.")
        return self.data

    def _collect_tweets(self, scrape_poster_details, no_tweets_limit):
        tweet_cards = self.driver.find_elements(
            "xpath", '//article[@data-testid="tweet" and not(@disabled)]'
        )
        if not tweet_cards:
            sleep(1)
            return

        for card in tweet_cards:
            try:
                card_id = str(card.id)  # or str(card._id) in older Selenium
                if card_id not in self.tweet_ids:
                    self.tweet_ids.add(card_id)
                    # Scroll into view for stability
                    self.driver.execute_script("arguments[0].scrollIntoView();", card)

                    tweet_obj = Tweet(
                        card=card,
                        driver=self.driver,
                        actions=self.actions,
                        scrape_poster_details=scrape_poster_details,
                    )
                    if tweet_obj and not tweet_obj.error and not tweet_obj.is_ad:
                        self.data.append(tweet_obj.to_dict())
                        if len(self.data) >= self.max_tweets and not no_tweets_limit:
                            self.scroller.scrolling = False
                            break
            except StaleElementReferenceException:
                continue

        # Scroll to load more
        self.scroller.scroll_to_bottom()
        sleep(2)

    def _dismiss_cookies_banner(self):
        try:
            cookies_btn = self.driver.find_element(
                "xpath", "//span[text()='Refuse non-essential cookies']/../../.."
            )
            cookies_btn.click()
        except NoSuchElementException:
            pass

    def _go_to_home(self):
        self.driver.get("https://twitter.com/home")
        sleep(2)

    def _go_to_profile(self, username):
        username = username.lstrip("@")
        self.driver.get(f"https://twitter.com/{username}")
        sleep(2)

    def _go_to_hashtag(self, hashtag, scrape_latest, scrape_top):
        hashtag = hashtag.lstrip("#")
        url = f"https://twitter.com/hashtag/{hashtag}?src=hashtag_click"
        if scrape_latest:
            url += "&f=live"
        self.driver.get(url)
        sleep(2)

    def _go_to_search(self, query, scrape_latest, scrape_top):
        url = f"https://twitter.com/search?q={query}&src=typed_query"
        if scrape_latest:
            url += "&f=live"
        self.driver.get(url)
        sleep(2)

    def save_data(self, output_file="tweets.csv"):
        """
        Save the scraped data to CSV or JSON.
        """
        if output_file.lower().endswith(".csv"):
            utils.save_to_csv(self.data, output_file=output_file)
        elif output_file.lower().endswith(".json"):
            utils.save_to_json(self.data, output_file=output_file)
        else:
            logging.warning("Unrecognized file extension, defaulting to .csv")
            utils.save_to_csv(self.data, output_file=output_file)
