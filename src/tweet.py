# src/tweet.py
from time import sleep
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement


class Tweet:
    def __init__(
        self,
        card: WebElement,
        driver,
        actions: ActionChains,
        scrape_poster_details=False,
    ) -> None:
        self.card = card
        self.driver = driver
        self.actions = actions
        self.scrape_poster_details = scrape_poster_details

        self.error = False
        self.is_ad = False

        # Initialize tweet data fields
        self.user = "skip"
        self.handle = "skip"
        self.date_time = "skip"
        self.verified = False
        self.content = ""
        self.reply_cnt = "0"
        self.retweet_cnt = "0"
        self.like_cnt = "0"
        self.analytics_cnt = "0"
        self.tags = []
        self.mentions = []
        self.emojis = []
        self.profile_img = ""
        self.tweet_link = ""
        self.tweet_id = ""
        self.user_id = None
        self.following_cnt = "0"
        self.followers_cnt = "0"

        # Extract basic tweet info
        self._extract_basic_info()

        # If critical info is missing or an error was flagged, do not continue
        if self.error:
            return

        # Optionally scrape more details (user_id, following/followers) by hovering
        if scrape_poster_details:
            self._extract_poster_details()

    def _extract_basic_info(self):
        # User
        try:
            self.user = self.card.find_element(
                "xpath", './/div[@data-testid="User-Name"]//span'
            ).text
        except NoSuchElementException:
            self.error = True

        # Handle
        try:
            self.handle = self.card.find_element(
                "xpath", './/span[contains(text(), "@")]'
            ).text
        except NoSuchElementException:
            self.error = True

        # Date/time
        try:
            self.date_time = self.card.find_element("xpath", ".//time").get_attribute(
                "datetime"
            )
            if self.date_time is not None:
                self.is_ad = False
        except NoSuchElementException:
            self.is_ad = True
            self.error = True

        # Verified check
        if not self.error:
            try:
                self.card.find_element(
                    "xpath", './/*[local-name()="svg" and @data-testid="icon-verified"]'
                )
                self.verified = True
            except NoSuchElementException:
                self.verified = False

        # Tweet text
        if not self.error:
            text_parts = self.card.find_elements(
                "xpath",
                '(.//div[@data-testid="tweetText"])[1]/span | (.//div[@data-testid="tweetText"])[1]/a',
            )
            self.content = "".join([part.text for part in text_parts])

        # Reply, retweet, like counts
        if not self.error:
            self.reply_cnt = self._get_text_or_default(
                './/button[@data-testid="reply"]//span', "0"
            )
            self.retweet_cnt = self._get_text_or_default(
                './/button[@data-testid="retweet"]//span', "0"
            )
            self.like_cnt = self._get_text_or_default(
                './/button[@data-testid="like"]//span', "0"
            )
            self.analytics_cnt = self._get_text_or_default(
                './/a[contains(@href, "/analytics")]//span', "0"
            )

        # Hashtags
        if not self.error:
            try:
                hashtag_elems = self.card.find_elements(
                    "xpath", './/a[contains(@href, "src=hashtag_click")]'
                )
                self.tags = [tag.text for tag in hashtag_elems]
            except NoSuchElementException:
                self.tags = []

        # Mentions
        if not self.error:
            try:
                mention_elems = self.card.find_elements(
                    "xpath",
                    '(.//div[@data-testid="tweetText"])[1]//a[contains(text(), "@")]',
                )
                self.mentions = [m.text for m in mention_elems]
            except NoSuchElementException:
                self.mentions = []

        # Emojis
        if not self.error:
            try:
                raw_emojis = self.card.find_elements(
                    "xpath",
                    '(.//div[@data-testid="tweetText"])[1]/img[contains(@src, "emoji")]',
                )
                self.emojis = [
                    e.get_attribute("alt").encode("unicode-escape").decode("ASCII")
                    for e in raw_emojis
                ]
            except NoSuchElementException:
                self.emojis = []

        # Profile image
        if not self.error:
            try:
                self.profile_img = self.card.find_element(
                    "xpath", './/div[@data-testid="Tweet-User-Avatar"]//img'
                ).get_attribute("src")
            except NoSuchElementException:
                self.profile_img = ""

        # Tweet link & tweet ID
        if not self.error:
            try:
                self.tweet_link = self.card.find_element(
                    "xpath", ".//a[contains(@href, '/status/')]"
                ).get_attribute("href")
                self.tweet_id = (
                    self.tweet_link.split("/")[-1] if self.tweet_link else ""
                )
            except NoSuchElementException:
                self.tweet_link = ""
                self.tweet_id = ""

    def _extract_poster_details(self):
        # Hover over user name to get user_id, following/followers
        try:
            el_name = self.card.find_element(
                "xpath", './/div[@data-testid="User-Name"]//span'
            )

            hover_attempts = 0
            details_extracted = False

            while hover_attempts < 3 and not details_extracted:
                try:
                    self.actions.move_to_element(el_name).perform()
                    hover_card = self.driver.find_element(
                        "xpath", '//div[@data-testid="hoverCardParent"]'
                    )

                    # user_id from data-testid
                    self._extract_user_id(hover_card)

                    # following/followers
                    self.following_cnt = self._get_text_or_default(
                        './/a[contains(@href, "/following")]//span', "0", hover_card
                    )
                    self.followers_cnt = self._get_text_or_default(
                        './/a[contains(@href, "/verified_followers")]//span',
                        "0",
                        hover_card,
                    )
                    details_extracted = True
                    self.actions.reset_actions()
                except NoSuchElementException:
                    hover_attempts += 1
                except StaleElementReferenceException:
                    self.error = True
                    return
        except NoSuchElementException:
            pass

    def _extract_user_id(self, hover_card):
        try:
            raw_user_id = hover_card.find_element(
                "xpath",
                '(.//div[contains(@data-testid, "-follow")]) | (.//div[contains(@data-testid, "-unfollow")])',
            ).get_attribute("data-testid")
            self.user_id = raw_user_id.split("-")[0] if raw_user_id else None
        except NoSuchElementException:
            pass

    def _get_text_or_default(self, xpath_expr, default_val, parent=None):
        if parent is None:
            parent = self.card
        try:
            val = parent.find_element("xpath", xpath_expr).text
            return val if val else default_val
        except NoSuchElementException:
            return default_val

    def to_dict(self):
        """
        Returns a dictionary representation of the tweet data.
        """
        return {
            "user": self.user,
            "handle": self.handle,
            "date_time": self.date_time,
            "verified": self.verified,
            "content": self.content,
            "reply_count": self.reply_cnt,
            "retweet_count": self.retweet_cnt,
            "like_count": self.like_cnt,
            "analytics_count": self.analytics_cnt,
            "tags": self.tags,
            "mentions": self.mentions,
            "emojis": self.emojis,
            "profile_img": self.profile_img,
            "tweet_link": self.tweet_link,
            "tweet_id": self.tweet_id,
            "user_id": self.user_id,
            "following_cnt": self.following_cnt,
            "followers_cnt": self.followers_cnt,
        }
