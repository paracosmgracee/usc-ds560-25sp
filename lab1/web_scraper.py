from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from pathlib import Path

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    chromedriver_path = '/usr/bin/chromedriver'
    service = Service(executable_path=chromedriver_path)
    
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error initializing Chrome driver: {e}")
        raise

def scrape_cnbc():
    url = "https://www.cnbc.com/world/"
    driver = None
    
    try:
        print("Initializing Chrome driver...")
        driver = setup_driver()
        
        print("Fetching data from CNBC...")
        driver.get(url)
        
        print("Waiting for page to load...")
        time.sleep(10)
        
        html_content = driver.page_source
        
        data_dir = Path("../data/raw_data")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = data_dir / "web_data.html"
        output_path.write_text(html_content, encoding='utf-8')
        print(f"Data successfully saved to {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    
    finally:
        if driver:
            try:
                driver.quit()
                print("Chrome driver closed successfully")
            except Exception as e:
                print(f"Error closing Chrome driver: {e}")

if __name__ == "__main__":
    scrape_cnbc()