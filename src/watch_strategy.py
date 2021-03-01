import logging
from selenium.webdriver.remote.webdriver import WebDriver
import random
from datetime import datetime, timedelta

from src.youtube import do_search, get_channel_videos, watch_current_video


def watch_strategy(driver: WebDriver, search_terms: list, channel_url: str, duration: int = 60):
    """Watches YouTube videos found by searching the provided search_terms and from the given channel_url, for a duration in minutes."""

    start_time = datetime.now()
    # Watch for the duration
    while datetime.now() < (start_time + timedelta(minutes=duration)):
        video_chooser = lambda: random.choice(
            [
                # Pick a random video from the channel
                random.choice(get_channel_videos(driver, channel_url)),
                # Pick a random video from a random search term
                random.choice(do_search(driver, random.choice(search_terms))),
            ]
        )

        video = video_chooser()
        logging.info(f"Watching {video.title}")
        # Watch the video
        driver.get(video.url)
        watch_current_video(driver)
