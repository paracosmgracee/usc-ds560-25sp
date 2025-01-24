import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_cards():
    url = "https://myperfectitinerary.com/category/itineraries/"
    driver = initialize_driver()
    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    data = []

    # Find all card elements
    cards = soup.find_all("a", class_="penci-image-holder penci-lazy")
    for card in cards:
        title = card["title"].strip() if "title" in card.attrs else "No Title"
        link = card["href"].strip() if "href" in card.attrs else "No Link"
        data.append({"Title": title, "Link": link})

    df = pd.DataFrame(data)
    csv_path = "itineraries_cards.csv"
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print("Data has been saved to itineraries_cards.csv!")
    return csv_path

# Data exploration
def explore_dataset(csv_path):
    try:
        df = pd.read_csv(csv_path)

        print("\n--- First Few Records ---")
        print(df.head())
        print("\n--- Dataset Size and Dimensions ---")
        print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        print("\n--- Missing Data ---")
        print(df.isnull().sum())
    except Exception as e:
        print(f"Error exploring dataset: {e}")

if __name__ == "__main__":
    csv_path = scrape_cards()
    explore_dataset(csv_path)
