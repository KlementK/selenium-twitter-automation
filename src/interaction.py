# src/interaction.py
import logging
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def like_tweet(driver, tweet_id: str):
    """
    Like a tweet by visiting its URL or locating it on the page.
    """
    logging.info(f"Attempting to like tweet ID {tweet_id}")
    tweet_url = f"https://twitter.com/anyuser/status/{tweet_id}"
    driver.get(tweet_url)
    sleep(2)

    try:
        like_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="like"]')
        like_button.click()
        logging.info(f"Tweet {tweet_id} liked successfully.")
    except NoSuchElementException:
        logging.error(
            "Like button not found. Possibly invalid Tweet ID or DOM changed."
        )


def comment_on_tweet(driver, actions, tweet_id: str, text: str):
    """
    Comment on a specific tweet by focusing on the 'Post your reply' field.
    """
    logging.info(f"Attempting to comment on tweet ID {tweet_id}")

    # Navigate directly to the tweet URL
    tweet_url = f"https://twitter.com/anyuser/status/{tweet_id}"
    driver.get(tweet_url)

    sleep(3)

    try:
        # cookie banner dismiss
        dismiss_cookie_banner(driver)

        # Wait for the 'Post your reply' placeholder to appear/clickable
        wait = WebDriverWait(driver, 10)

        reply_field = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//div[contains(@class,"public-DraftEditorPlaceholder-inner") '
                    'and contains(text(),"Post your reply")]',
                )
            )
        )

        logging.info("Clicking the reply field to focus...")
        reply_field.click()
        sleep(2)

        logging.info("Typing comment text via ActionChains...")
        actions.send_keys(text).perform()
        sleep(1)

        logging.info("Submitting comment (Ctrl+Enter)...")
        actions.key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(
            Keys.CONTROL
        ).perform()
        sleep(2)

        logging.info(f"Comment posted on tweet {tweet_id}.")
    except TimeoutException:
        logging.error("The 'Post your reply' field never became clickable in time.")
    except NoSuchElementException:
        logging.error("Could not find the 'Post your reply' placeholder in the DOM.")


def retweet_tweet(driver, tweet_id: str):
    """
    Retweet a specific tweet.
    """
    logging.info(f"Attempting to retweet tweet ID {tweet_id}")
    tweet_url = f"https://twitter.com/anyuser/status/{tweet_id}"
    driver.get(tweet_url)
    sleep(2)

    try:
        retweet_button = driver.find_element("xpath", '//div[@data-testid="retweet"]')
        retweet_button.click()
        sleep(1)

        confirm_button = driver.find_element(
            "xpath", '//div[@data-testid="retweetConfirm"]'
        )
        confirm_button.click()

        logging.info(f"Tweet {tweet_id} retweeted successfully.")
    except NoSuchElementException:
        logging.error(
            "Retweet elements not found. Possibly invalid Tweet ID or DOM changed."
        )


def quote_tweet(driver, tweet_id: str, quote_text: str):
    """
    Quote a specific tweet with additional text.
    """
    logging.info(f"Attempting to quote tweet ID {tweet_id}")
    tweet_url = f"https://twitter.com/anyuser/status/{tweet_id}"
    driver.get(tweet_url)
    sleep(2)

    try:
        retweet_button = driver.find_element("xpath", '//div[@data-testid="retweet"]')
        retweet_button.click()
        sleep(1)

        quote_option = driver.find_element(
            "xpath", '//div[@data-testid="retweetWithComment"]'
        )
        quote_option.click()
        sleep(1)

        quote_box = driver.find_element(
            "xpath", '//div[@data-testid="tweetTextarea_0"]'
        )
        quote_box.send_keys(quote_text)
        sleep(1)

        quote_box.send_keys(Keys.CONTROL + Keys.ENTER)
        logging.info(f"Quoted tweet {tweet_id} with text: {quote_text}")
    except NoSuchElementException:
        logging.error(
            "Quote tweet elements not found. Possibly invalid tweet ID or DOM changed."
        )


def dismiss_cookie_banner(driver):
    try:
        cookie_banner_button = driver.find_element(
            By.XPATH, "//span[text()='Refuse non-essential cookies']/../../.."
        )
        cookie_banner_button.click()
        sleep(1)
    except NoSuchElementException:
        pass
