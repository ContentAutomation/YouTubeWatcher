import argparse
import logging
from src.youtube import close_privacy_popup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from argparse import ArgumentError
from datetime import datetime

from src.docker_tor import get_current_ip, get_new_ip
from src.watch_strategy import watch_strategy


def main():
    logging.getLogger().setLevel(logging.INFO)

    # Setup Selenium web driver
    parser = get_arg_parser()
    args = parser.parse_args()

    if args.browser == "docker":
        # Tor is the default when using docker
        if not hasattr(args, "useTor") or args.useTor:
            options = get_firefox_tor_config().to_capabilities()
        else:
            options = get_firefox_config().to_capabilities()

        driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            desired_capabilities=options,
        )
    elif args.browser == "firefox":
        if args.useTor:
            logging.warning("Using local Firefox with Tor. The watcher will not be able to renew the Tor ip!")
        driver = webdriver.Firefox(options=get_firefox_config())
    elif args.browser == "chrome":
        driver = webdriver.Chrome()
    else:
        raise ArgumentError(message="Unknown driver.")

    try:
        # Log our current ip to make sure Tor is working as intended
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
            if args.browser == "docker":
                # After watching for an hour, get a new ip address.
                # And what ever happens, just fix it by restarting tor!
                # And if you're not using docker, you'll have to reset tor yourself.
                logging.info("Getting new Tor ip.")
                driver = get_new_ip(get_firefox_tor_config())
            else:
                logging.warning("Using local Firefox with Tor. The watcher was not able to renew the Tor ip!")
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


def get_firefox_tor_config() -> webdriver.FirefoxOptions:
    """Configure Firefox for usage with tor"""
    firefox_options = get_firefox_config()
    # Configure the proxy for tor
    firefox_options.set_preference("network.proxy.type", 1)
    firefox_options.set_preference("network.proxy.socks_version", 5)
    # Tor runs in the same container as firefox, so we can connect to tor with localhost:9050
    firefox_options.set_preference("network.proxy.socks", "127.0.0.1")
    firefox_options.set_preference("network.proxy.socks_port", 9050)
    firefox_options.set_preference("network.proxy.socks_remote_dns", True)
    return firefox_options


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    today = datetime.now()
    parser.add_argument(
        "-B",
        "--browser",
        choices=["docker", "chrome", "firefox"],
        default="docker",
        type=str,
        help="Select the driver/browser to use for executing the script.",
    )
    parser.add_argument(
        "-t",
        "--enable-tor",
        action="store_true",
        dest="use_tor",
        default=None,
        help="Enables Tor usage by connecting to a proxy on localhost:9050. Only usable with the docker executor.",
    )
    parser.add_argument("--disable-tor", action="store_false", dest="use_tor", help="Disables the Tor proxy.")
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
