import argparse
import logging
from argparse import ArgumentError

from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from src.docker_firefox import get_current_ip
from src.watch_strategy import watch_strategy
from src.youtube import close_privacy_popup


def main():
    logging.getLogger().setLevel(logging.INFO)

    # Setup Selenium web driver
    parser = get_arg_parser()
    args = parser.parse_args()

    if args.browser == "docker":
        options = get_firefox_config().to_capabilities()

        driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            desired_capabilities=options,
        )
    elif args.browser == "firefox":
        driver = webdriver.Firefox(options=get_firefox_config())
    elif args.browser == "chrome":
        driver = webdriver.Chrome()
    else:
        raise ArgumentError(message="Unknown driver.")

    try:
        # Log our current ip
        logging.info(f"Current IP: {get_current_ip(driver)}")
        # Start watching videos
        while True:
            try:
                # Consent to YouTube's cookies
                close_privacy_popup(driver)
                watch_strategy(driver, args.search_terms, args.channel_url, duration=60)
            except TimeoutException:
                logging.warning("Probably getting a Captcha because of blocked IP, restarting Docker")
                pass
            except Exception as e:
                logging.error(repr(e))
                pass
    except:
        # Make sure the driver doesn't leak no matter what
        driver.quit()
        raise


def get_firefox_config() -> webdriver.FirefoxOptions:
    """Configure firefox for automated watching"""
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.set_preference("intl.accept_languages", "en-us")
    # Always autoplay videos
    firefox_options.set_preference("media.autoplay.default", 0)
    firefox_options.set_preference("media.volume_scale", "0.0")
    return firefox_options


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-B",
        "--browser",
        choices=["docker", "chrome", "firefox"],
        default="docker",
        type=str,
        help="Select the driver/browser to use for executing the script.",
    )
    parser.add_argument(
        "-s",
        "--search-terms",
        dest="search_terms",
        action="append",
        help="This argument declares a list of search terms which get viewed.",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--channel-url",
        default="https://www.youtube.com/channel/UCqq27nknJ3fe5IvrAbfuEwQ",
        dest="channel_url",
        type=str,
        help="Channel URL if not declared it uses Golden Gorillas channel URL as default.",
        required=False,
    )
    return parser


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Quitting watcher")
