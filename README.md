<p align="center">
    <a href="https://github.com/ContentAutomation"><img src="https://contentautomation.s3.eu-central-1.amazonaws.com/logo.png" alt="Logo" width="150"/></a>
    <br />
    <br />
    <a href="http://choosealicense.com/licenses/mit/"><img src="https://img.shields.io/badge/license-MIT-3C93B4.svg?style=flat" alt="MIT License"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
    <br />
    <a href="https://www.youtube.com/channel/UCqq27nknJ3fe5IvrAbfuEwQ"><img src="https://img.shields.io/badge/YouTube-FF0000.svg?style=flat&logo=youtube" alt="Platform: YouTube"></a>
    <br />
    <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-%F0%9F%90%B3-%232391e6" alt="Uses Docker"></a>
    <a href="https://www.selenium.dev/documentation/en/"><img src="https://img.shields.io/badge/Selenium-Firefox%20%7C%20Chrome-%23f17d3e" alt="Automation supporting Firefox and Chrome"></a>
    <a href="https://www.torproject.org/"><img src="https://img.shields.io/badge/Tor-%F0%9F%A7%85-%23794493" alt="Uses Tor. And an emoji of an onion, get it?"></a>
    <br />
    <br />
    <i>An automated, headless YouTube Watcher and Scraper</i>
    <br />
<br />
    <i><b>Authors</b>:
        <a href="https://github.com/ChristianCoenen">Christian C.</a>,
        <a href="https://github.com/MorMund">Moritz M.</a>,
        <a href="https://github.com/lucaSchilling">Luca S. </a>
    </i>
</p>
<hr />

Search YouTube, query recommended videos and watch them. All fully automated and anonymised through the [Tor network](https://www.torproject.org/). The project consists of two independently usable components, the YouTube automation written in Python and the dockerized Tor Browser.

## YouTube automation

### Setup

This project requires [Poetry](https://python-poetry.org/) to install the required dependencies.
Check out [this link](https://python-poetry.org/docs/) to install Poetry on your operating system.

Make sure you have installed [Python](https://www.python.org/downloads/) 3.8 or higher! Otherwise Step 3 will let you know that you have no compatible Python version installed.

1. Clone/Download this repository
2. Navigate to the root of the repository
3. Run ```poetry install``` to create a virtual environment with Poetry
4. Either run the dockerized Browser with `docker-compose up`, install [geckodriver](https://github.com/mozilla/geckodriver/releases) for a local Firefox or [ChromeDriver](https://chromedriver.chromium.org/downloads) for Chromium. Ensure that geckodriver/ChromeDriver are in a location in your `$PATH`.
5. Run ```poetry run python main.py``` to run the program. Alternatively you can run ```poetry shell``` followed by ```python main.py```. By default this connects to the dockerized Browser. To automate a different Browser use `--browser [chrome/firefox]` command line option.

## Run Parameters
All of these parameters are optional and a default value will be used if they are not defined. 
You can also get these definitions by running ```main.py --help```