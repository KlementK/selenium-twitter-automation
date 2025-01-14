# src/scroller.py
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


class Scroller:
    def __init__(self, driver) -> None:
        """
        Initializes the Scroller with the given WebDriver.

        :param driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.current_position = 0
        self.last_position = self.get_current_scroll_position()
        self.scrolling = True
        self.scroll_count = 0

    def get_current_scroll_position(self) -> int:
        """
        Returns the current vertical scroll position of the page.

        :return: Current scroll position (in pixels)
        """
        return self.driver.execute_script("return window.pageYOffset;")

    def reset(self) -> None:
        """
        Resets the scrolling position and scroll count.
        """
        self.current_position = 0
        self.last_position = self.get_current_scroll_position()
        self.scroll_count = 0
        logging.info("Scroller reset.")

    def scroll_to_top(self) -> None:
        """
        Scrolls the page to the top.
        """
        self.driver.execute_script("window.scrollTo(0, 0);")
        logging.info("Scrolled to top.")

    def scroll_to_bottom(self) -> None:
        """
        Scrolls the page to the bottom.
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logging.info("Scrolled to bottom.")

    def update_scroll_position(self) -> None:
        """
        Updates the current scroll position and increments the scroll count if the position has changed.
        """
        new_position = self.get_current_scroll_position()
        if new_position != self.current_position:
            self.current_position = new_position
            self.scroll_count += 1
            logging.info(
                f"Scroll position updated: {self.current_position} (Scroll count: {self.scroll_count})"
            )
