import os
import time
from pathlib import Path
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

BASE_DIR = Path(os.path.abspath(__file__)).parent.parent

def main():
    # 1) Configure Selenium Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 2) Specify the path to chromedriver
    service = Service(executable_path="/usr/bin/chromedriver")

    # 3) Initialize the Chrome WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 4) Open the target webpage
        url = "https://www.cnbc.com/world/?region=world"
        print(f"Opening page: {url}")
        driver.get(url)

        # 5) Wait for the page to load
        time.sleep(5)

        # 6) Retrieve the rendered HTML
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # 7) Save HTML to data/raw_data/web_data.html
        raw_data_dir = BASE_DIR / "data" / "raw_data"
        raw_data_dir.mkdir(parents=True, exist_ok=True)
        output_file = raw_data_dir / "web_data.html"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(soup.prettify())

        print(f"HTML data saved to: {output_file}")

        # 8) Print the first 10 lines to meet assignment requirements
        print("\nPrinting first 10 lines of web_data.html:\n")
        with open(output_file, "r", encoding="utf-8") as f:
            for i in range(10):
                line = f.readline()
                if not line:
                    break
                print(line.rstrip())

    finally:
        # 9) Quit the driver
        driver.quit()

if __name__ == "__main__":
    main()