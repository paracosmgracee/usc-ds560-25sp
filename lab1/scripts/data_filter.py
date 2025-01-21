import os
from pathlib import Path
import csv
from bs4 import BeautifulSoup

BASE_DIR = Path(os.path.abspath(__file__)).parent.parent

def extract_market_data(soup):
    """
    Extract 3 fields for market data:
      - MarketCard-symbol
      - MarketCard-stockPosition
      - MarketCard-changesPct
    
    Based on the structure:
        <section class="MarketsBanner--container" id="Homepage_MarketsBanner-1" data-test="marketsBanner-1-0" data-analytics="Homepage-marketsBanner-1-0">
        <div class="MarketsBannerMenu--marketBannerMenuWrapper">
        </div>

        <div class="MarketsBanner--main">
            <div id="market-data-scroll-container" class="MarketsBanner--marketData flex">
            
            <!-- Market Card: DJIA -->
            <a href="//www.cnbc.com/quotes/.DJIA" class="MarketCard-container MarketCard-up MarketCard-wrap">
                <div class="MarketCard-row flex">
                <span class="MarketCard-symbol">DJIA</span>
                <span class="MarketCard-stockPosition">43,487.83</span>
                </div>
                <div class="MarketCard-row flex">
                <!-- Possibly some change data here -->
                </div>
                <div class="MarketCard-row flex">
                <!-- Possibly more info or timestamp -->
                </div>
            </a>

            <!-- Market Card: S&P 500 -->
            <a href="//www.cnbc.com/quotes/.SPX" class="MarketCard-container MarketCard-up MarketCard-wrap">
                <div class="MarketCard-row flex">
                <span class="MarketCard-symbol">S&P 500</span>
                <span class="MarketCard-stockPosition">4,012.32</span>
                </div>
                <div class="MarketCard-row flex">
                <!-- Additional details -->
                </div>
            </a>

            </div>
        </div>
        </section>
    """
    market_data = []
    try:
        # 1) Locate the container <div id="market-data-scroll-container">
        container = soup.find("div", id="market-data-scroll-container")
        if not container:
            print("Warning: Could not find container with id='market-data-scroll-container'.")
            return market_data

        # 2) Find all cards: <a class="MarketCard-container ..."> or <div class="MarketCard-container ...">
        cards = container.find_all(
            lambda tag: tag.name in ["a", "div"]
            and tag.has_attr("class")
            and "MarketCard-container" in tag["class"]
        )
        if not cards:
            print("Warning: No market cards found.")
            return market_data

        # 3) Extract symbol, stockPosition, and changesPct
        for card in cards:
            symbol_tag = card.find("span", class_="MarketCard-symbol")
            position_tag = card.find("span", class_="MarketCard-stockPosition")
            pct_tag = card.find("span", class_="MarketCard-changesPct")

            symbol_text = symbol_tag.get_text(strip=True) if symbol_tag else ""
            position_text = position_tag.get_text(strip=True) if position_tag else ""
            pct_text = pct_tag.get_text(strip=True) if pct_tag else ""

            market_data.append([symbol_text, position_text, pct_text])

    except Exception as e:
        print(f"Error extracting market data: {e}")
    
    return market_data


def extract_news_data(soup):
    """
    Extract fields from the 'Latest News' section:
      - LatestNews-timestamp
      - title
      - link

    Based on the structure:
        <ul class="LatestNews-list">
            <li class="LatestNews-item">
            <div class="LatestNews-container">
                <time class="LatestNews-timestamp">...</time>
                <a href="..." class="LatestNews-headline">...</a>
            </div>
            </li>
        </ul>
    """
    news_data = []
    try:
        # 1) Locate the <ul class="LatestNews-list">
        news_container = soup.find("ul", class_="LatestNews-list")
        if not news_container:
            print("Warning: Could not find <ul class='LatestNews-list'>.")
            return news_data

        # 2) Find all <li class="LatestNews-item">
        items = news_container.find_all("li", class_="LatestNews-item")
        if not items:
            print("Warning: No news items found under <ul class='LatestNews-list'>.")
            return news_data

        # 3) Extract timestamp, title, and link
        for item in items:
            time_tag = item.find("time", class_="LatestNews-timestamp")
            timestamp = time_tag.get_text(strip=True) if time_tag else ""

            link_tag = item.find("a", class_="LatestNews-headline")
            title = link_tag.get_text(strip=True) if link_tag else ""
            href = link_tag.get("href", "") if link_tag else ""

            news_data.append([timestamp, title, href])

    except Exception as e:
        print(f"Error extracting news data: {e}")

    return news_data


def main():
    print("Reading web_data.html...")

    # Prepare directories
    raw_data_dir = BASE_DIR / "data" / "raw_data"
    processed_data_dir = BASE_DIR / "data" / "processed_data"
    processed_data_dir.mkdir(parents=True, exist_ok=True)

    web_data_file = raw_data_dir / "web_data.html"
    if not web_data_file.exists():
        print("Error: web_data.html not found. Please run web_scraper_selenium.py first.")
        return

    # Parse the HTML with BeautifulSoup
    with open(web_data_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # ============ Extract and save market data ============
    print("Filtering market data fields...")
    market_data = extract_market_data(soup)
    print(f"Found {len(market_data)} market items.")

    market_csv = processed_data_dir / "market_data.csv"
    market_headers = ["Symbol", "StockPosition", "ChangePct"]

    if not market_data:
        print(f"Warning: No data to write to {market_csv}")
    else:
        try:
            with open(market_csv, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(market_headers)
                writer.writerows(market_data)
            print(f"Successfully created {market_csv}")
        except Exception as e:
            print(f"Error saving to CSV {market_csv}: {e}")

    # ============ Extract and save latest news ============
    print("Filtering latest news fields...")
    news_data = extract_news_data(soup)
    print(f"Found {len(news_data)} news items.")

    news_csv = processed_data_dir / "news_data.csv"
    news_headers = ["Timestamp", "Title", "Link"]

    if not news_data:
        print(f"Warning: No data to write to {news_csv}")
    else:
        try:
            with open(news_csv, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(news_headers)
                writer.writerows(news_data)
            print(f"Successfully created {news_csv}")
        except Exception as e:
            print(f"Error saving to CSV {news_csv}: {e}")

    print("Data filtering complete!")


if __name__ == "__main__":
    main()
