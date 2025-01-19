from bs4 import BeautifulSoup
import csv
import os
from pathlib import Path

def extract_market_data(soup):
    market_data = []
    
    try:
        market_containers = soup.find_all('div', class_='marketCard')
        
        for container in market_containers:
            symbol = container.find('div', class_='marketCard_symbol').text.strip()
            value = container.find('div', class_='marketCard_stockPosition').text.strip()
            change = container.find('div', class_='marketCard-changePct').text.strip()
            market_data.append([symbol, value, change])
    
    except Exception as e:
        print(f"Error extracting market data: {e}")
    
    return market_data

def extract_news_data(soup):
    news_data = []
    try:
        news_containers = soup.find_all(['div', 'article'], class_=lambda x: x and any(name in str(x).lower() for name in [
            'latestnews', 'latest-news', 'news-item', 'latesnews-item'
        ]))
        
        for item in news_containers:
            timestamp = (
                item.find('span', class_='LatestNews-timestamp') or
                item.find('time') or
                item.find('span', class_='timestamp')
            )
            timestamp = timestamp.text.strip() if timestamp else ""
            
            headline = (
                item.find('a', class_='headline') or
                item.find('a') or
                item.find('h3 a')
            )
            
            title = headline.text.strip() if headline else ""
            link = headline['href'] if headline and headline.has_attr('href') else ""
            
            if any([timestamp, title, link]):
                news_data.append([timestamp, title, link])
    
    except Exception as e:
        print(f"Error extracting news data: {e}")
    
    return news_data

def save_to_csv(data, filename, headers):
    try:
        if not data:
            print(f"Warning: No data to write to {filename}")
            return
            
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"Successfully created {filename}")
    except Exception as e:
        print(f"Error saving to CSV {filename}: {e}")

def main():
    try:
        data_dir = Path("../data/processed_data")
        data_dir.mkdir(parents=True, exist_ok=True)

        print("Reading web_data.html...")
        with open("../data/raw_data/web_data.html", 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        print("Filtering market and news data fields...")
        market_data = extract_market_data(soup)
        market_headers = ["Symbol", "Value", "Change"]
        save_to_csv(
            market_data,
            str(data_dir / "market_data.csv"),
            market_headers
        )

        news_data = extract_news_data(soup)
        news_headers = ["Timestamp", "Title", "Link"]
        save_to_csv(
            news_data,
            str(data_dir / "news_data.csv"),
            news_headers
        )

        print("Data filtering complete!")

    except FileNotFoundError:
        print("Error: web_data.html file not found in raw_data directory")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()