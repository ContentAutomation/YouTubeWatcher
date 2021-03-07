from typing import Union

from selenium.webdriver.remote.webelement import WebElement


class ClickableVideoElement:
    """Parser for an Element on YouTube that can be clicked by the user to watch a video, e.g. a search result.
    Supported video elements are ytd-video-renderer,ytd-compact-video-renderer and ytd-grid-video-renderer

    Attributes:
        title - Video title
        url - URL of the video
        channel_name - Name of the Uploader
        channel_url - If available, the URL to the uploader's channel
    """

    def __init__(self, video_element: WebElement, channel_name: str = None):
        self.title: str = None
        self.url: str = None
        self.channel_name: str = None
        self.channel_url: Union[str, None] = None
        self.element = video_element
        if video_element.tag_name == "ytd-video-renderer":
            self._parse_vid_render_elem(video_element)
        elif video_element.tag_name == "ytd-compact-video-renderer":
            self._parse_compact_render_elem(video_element)
        elif video_element.tag_name == "ytd-grid-video-renderer":
            self._parse_grid_render_elem(video_element, channel_name)
        else:
            raise NotImplementedError(f"Unknown video element type: {video_element.tag_name}")

    def _parse_vid_render_elem(self, video_element: WebElement):
        title_label = video_element.find_element_by_css_selector("a#video-title")
        self.title = title_label.get_attribute("title")
        self.url = title_label.get_attribute("href")

        channel_label = video_element.find_element_by_xpath(".//ytd-channel-name//a")
        self.channel_name = channel_label.get_attribute("innerText")
        self.channel_url = channel_label.get_attribute("href")

    def _parse_compact_render_elem(self, video_element: WebElement):
        self.title = video_element.find_element_by_css_selector("span#video-title").get_attribute("innerText")
        self.url = video_element.find_element_by_tag_name("a").get_attribute("href")
        self.channel_name = video_element.find_element_by_xpath(
            ".//ytd-channel-name//yt-formatted-string"
        ).get_attribute("innerText")
        self.channel_url = None  # Channel is not clickable from this element

    def _parse_grid_render_elem(self, video_element: WebElement, channel_name: str):
        title_label = video_element.find_element_by_css_selector("a#video-title")
        self.title = title_label.get_attribute("title")
        self.url = title_label.get_attribute("href")
        self.channel_name = channel_name
        self.channel_url = None  # Channel is not clickable from this element
