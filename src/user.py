# src/user.py
import logging
from time import sleep
from selenium.webdriver.common.keys import Keys

TWITTER_POST_URL = "https://twitter.com/compose/tweet"


class TwitterUser:
    """
    Manages user-related actions such as posting tweets, following, and unfollowing.
    """

    def __init__(self, driver, actions):
        """
        :param driver: Selenium WebDriver instance
        :param actions: Selenium ActionChains instance
        """
        self.driver = driver
        self.actions = actions

    def create_new_tweet(self, tweet_content):
        """
        Post a new tweet.
        """
        logging.info("Navigating to tweet creation page...")
        try:
            self.driver.get(TWITTER_POST_URL)
            sleep(3)

            logging.info(f"Entering tweet content: {tweet_content}")
            # Type the tweet
            self.actions.send_keys(tweet_content).perform()
            sleep(1)

            # Post the tweet (Ctrl+Enter or locate the Tweet button)
            logging.info("Posting the tweet...")
            self.actions.key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(
                Keys.CONTROL
            ).perform()
            sleep(2)

            logging.info("Tweet posted successfully.")
        except Exception as e:
            logging.error(f"Failed to create tweet: {e}", exc_info=True)

    def follow_user(self, username):
        """
        Follow a user by username.
        """
        try:
            username = username.lstrip("@")
            profile_url = f"https://twitter.com/{username}"
            self.driver.get(profile_url)
            sleep(3)

            follow_button = self.driver.find_element(
                "xpath", '//div[@data-testid="follow"]'
            )
            follow_button.click()
            logging.info(f"Followed user: {username}")
        except Exception as e:
            logging.error(f"Could not follow user {username}: {e}", exc_info=True)

    def unfollow_user(self, username):
        """
        Unfollow a user by username.
        """
        try:
            username = username.lstrip("@")
            profile_url = f"https://twitter.com/{username}"
            self.driver.get(profile_url)
            sleep(3)

            unfollow_button = self.driver.find_element(
                "xpath", '//div[@data-testid="unfollow"]'
            )
            unfollow_button.click()
            sleep(1)

            confirm_btn = self.driver.find_element(
                "xpath", '//div[@data-testid="confirmationSheetConfirm"]'
            )
            confirm_btn.click()

            logging.info(f"Unfollowed user: {username}")
        except Exception as e:
            logging.error(f"Could not unfollow user {username}: {e}", exc_info=True)

    def open_profile_page(self):
        """
        Open the currently logged-in user's profile page (Twitter often uses /home -> /profile).
        """
        self.driver.get("https://twitter.com/i/user")
        sleep(2)
        logging.info("Opened profile page.")
