import logging
import time

import docker
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


def get_new_ip(firefox_options: webdriver.FirefoxOptions, old_driver: WebDriver = None) -> WebDriver:
    if old_driver:
        old_driver.quit()
    client = docker.from_env()
    container = client.containers.get("firefox")
    container.restart()
    # Wait for our container to start
    time.sleep(60)
    driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4444/wd/hub",
        desired_capabilities=firefox_options.to_capabilities(),
    )

    logging.info(f"Current IP: {get_current_ip(driver)}")
    return driver


def get_current_ip(driver: WebDriver) -> str:
    """Get the browser's current ip by visiting myip.com"""
    driver.get("https://myip.com")
    return driver.find_element_by_css_selector("#ip").text
