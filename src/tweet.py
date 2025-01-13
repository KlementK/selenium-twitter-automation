import logging
from time import sleep
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains


# Constants for default values
SKIP = "skip"
ZERO = "0"


# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


class Tweet:
    def __init__(
        self,
        card: WebDriver,
        driver: WebDriver,
        actions: ActionChains,
        scrape_poster_details=False,
    ) -> None:
        """
        Initializes the Tweet object with tweet data from the card.

        :param card: The Selenium WebDriver element representing the tweet card.
        :param driver: The Selenium WebDriver instance for additional interactions.
        :param actions: The ActionChains object to handle user actions.
        :param scrape_poster_details: Flag to scrape additional user details (followers, following, etc.).
        """
        self.card = card
        self.error = False
        self.tweet = None

        # Extract basic tweet details
        self.extract_tweet_details()

        # Extract user details if required
        if scrape_poster_details:
            self.extract_user_details(driver, actions)

        if self.error:
            logging.error("Failed to extract tweet details.")
            return

        self.tweet = (
            self.user,
            self.handle,
            self.date_time,
            self.verified,
            self.content,
            self.reply_cnt,
            self.retweet_cnt,
            self.like_cnt,
            self.analytics_cnt,
            self.tags,
            self.mentions,
            self.emojis,
            self.profile_img,
            self.tweet_link,
            self.tweet_id,
            self.user_id,
            self.following_cnt,
            self.followers_cnt,
        )

    def get_element_text(self, card, xpath: str, default=ZERO) -> str:
        """
        Helper method to fetch text from an element or return a default value if not found.

        :param card: The Selenium WebDriver element representing the tweet card.
        :param xpath: The XPath of the element to find.
        :param default: The default value to return if the element is not found.
        :return: The text of the element or the default value.
        """
        retries = 3
        while retries > 0:
            try:
                return card.find_element("xpath", xpath).text or default
            except NoSuchElementException:
                return default
            except StaleElementReferenceException:
                retries -= 1
                logging.warning(
                    f"Stale element encountered. Retrying... ({3 - retries} attempts left)"
                )
                sleep(0.5)
        logging.error(
            f"Failed to find element with xpath: {xpath}. Giving up after 3 retries."
        )
        self.error = True
        return default

    def extract_tweet_details(self) -> None:
        """
        Extracts all tweet-related details such as content, likes, retweets, etc.
        """
        self.user = self.get_element_text(
            self.card, './/div[@data-testid="User-Name"]//span', SKIP
        )
        self.handle = self.get_element_text(
            self.card, './/span[contains(text(), "@")]', SKIP
        )
        self.date_time = self.get_element_text(self.card, ".//time", SKIP)

        # Check if the tweet is an ad
        self.is_ad = False if self.date_time != SKIP else True
        if self.is_ad:
            logging.info("This tweet is an ad.")

        self.verified = self.get_element_text(
            self.card,
            './/*[local-name()="svg" and @data-testid="icon-verified"]',
            False,
        )
        self.content = self.get_tweet_content()

        # Extract counts for replies, retweets, likes, and analytics
        self.reply_cnt = self.get_element_text(
            self.card, './/button[@data-testid="reply"]//span', ZERO
        )
        self.retweet_cnt = self.get_element_text(
            self.card, './/button[@data-testid="retweet"]//span', ZERO
        )
        self.like_cnt = self.get_element_text(
            self.card, './/button[@data-testid="like"]//span', ZERO
        )
        self.analytics_cnt = self.get_element_text(
            self.card, './/a[contains(@href, "/analytics")]//span', ZERO
        )

        # Extract tags and mentions
        self.tags = self.get_elements_text(
            self.card, './/a[contains(@href, "src=hashtag_click")]'
        )
        self.mentions = self.get_elements_text(
            self.card, '(.//div[@data-testid="tweetText"])[1]//a[contains(text(), "@")]'
        )

        # Extract emojis
        self.emojis = self.get_elements_text(
            self.card,
            '(.//div[@data-testid="tweetText"])[1]/img[contains(@src, "emoji")]',
        )

        # Extract profile image and tweet link
        self.profile_img = self.get_element_text(
            self.card, './/div[@data-testid="Tweet-User-Avatar"]//img', ""
        )
        self.tweet_link = self.get_element_text(
            self.card, ".//a[contains(@href, '/status/')]", ""
        )
        self.tweet_id = self.tweet_link.split("/")[-1] if self.tweet_link else ""

    def get_elements_text(self, card, xpath: str) -> list:
        """
        Helper method to fetch text from multiple elements using XPath.

        :param card: The Selenium WebDriver element representing the tweet card.
        :param xpath: The XPath to find the elements.
        :return: A list of element texts.
        """
        try:
            elements = card.find_elements("xpath", xpath)
            return [element.text for element in elements]
        except NoSuchElementException:
            return []

    def extract_user_details(self, driver, actions) -> None:
        """
        Extracts additional user details such as user ID, followers, and following counts.
        """
        el_name = self.card.find_element(
            "xpath", './/div[@data-testid="User-Name"]//span'
        )
        ext_hover_card = False
        ext_user_id = False
        ext_following = False
        ext_followers = False
        hover_attempt = 0

        while (
            not ext_hover_card
            or not ext_user_id
            or not ext_following
            or not ext_followers
        ):
            try:
                actions.move_to_element(el_name).perform()
                hover_card = driver.find_element(
                    "xpath", '//div[@data-testid="hoverCardParent"]'
                )
                ext_hover_card = True

                while not ext_user_id:
                    try:
                        raw_user_id = hover_card.find_element(
                            "xpath",
                            '(.//div[contains(@data-testid, "-follow")]) | (.//div[contains(@data-testid, "-unfollow")])',
                        ).get_attribute("data-testid")
                        self.user_id = (
                            raw_user_id.split("-")[0] if raw_user_id else None
                        )
                        ext_user_id = True
                    except NoSuchElementException:
                        continue
                    except StaleElementReferenceException:
                        self.error = True
                        return

                while not ext_following:
                    try:
                        self.following_cnt = (
                            hover_card.find_element(
                                "xpath", './/a[contains(@href, "/following")]//span'
                            ).text
                            or ZERO
                        )
                        ext_following = True
                    except NoSuchElementException:
                        continue
                    except StaleElementReferenceException:
                        self.error = True
                        return

                while not ext_followers:
                    try:
                        self.followers_cnt = (
                            hover_card.find_element(
                                "xpath",
                                './/a[contains(@href, "/verified_followers")]//span',
                            ).text
                            or ZERO
                        )
                        ext_followers = True
                    except NoSuchElementException:
                        continue
                    except StaleElementReferenceException:
                        self.error = True
                        return
            except NoSuchElementException:
                if hover_attempt == 3:
                    logging.error("Failed to retrieve user details after 3 attempts.")
                    self.error = True
                    return
                hover_attempt += 1
                sleep(0.5)
                continue
            except StaleElementReferenceException:
                self.error = True
                return

        if ext_hover_card and ext_following and ext_followers:
            actions.reset_actions()
            logging.info("User details successfully extracted.")
