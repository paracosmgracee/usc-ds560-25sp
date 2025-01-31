import yfinance as yf
from mysql_helper import *

create_database_query = "CREATE DATABASE IF NOT EXISTS DSCI560_Stocks"

tables_queries = [
    """
    CREATE TABLE IF NOT EXISTS Stocks_analysis (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        ticker VARCHAR(10) NOT NULL,
        sector VARCHAR(100),
        industry VARCHAR(100),
        pe_ratio DECIMAL(10,2),
        pb_ratio DECIMAL(10,2),
        de_ratio DECIMAL(10,2),
        roe DECIMAL(10,2),
        eps DECIMAL(10,2),
        dividend_yield DECIMAL(10,2)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS stock_history (
        stock_id INT NOT NULL,
        date DATE NOT NULL,
        open_price DECIMAL(10,2),
        high_price DECIMAL(10,2),
        low_price DECIMAL(10,2),
        close_price DECIMAL(10,2),
        volume BIGINT,
        dividend_amount DECIMAL(10,2),
        stock_split DECIMAL(10,2),
        insertion_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (stock_id, date, insertion_time),
        FOREIGN KEY (stock_id) REFERENCES Stocks(id)
    );
    """
]

stocks_to_collect = ['AAPL','NVDA']

def initialize_database():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(create_database_query)
    cursor.execute("USE DSCI560_Stocks")
    
    for query in tables_queries:
        cursor.execute(query)
    
    commit_and_close(connection)
    print("Database initialized successfully")
    
    
    
def collect_stock_history(ticker,period='1y'):
    connection = create_connection()
    cursor = connection.cursor()
    
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)
    
    cursor.execute("SELECT * FROM Stocks WHERE ticker = %s", [ticker])
    
    stock = cursor.fetchone()
    
    if not stock:
        return "Stock not found in database"
    stock_id = stock[0]
    
    
    
    for date, row in history.iterrows():
        cursor.execute("""
        INSERT INTO stock_history (stock_id,	date,	open_price,	high_price,	low_price,	close_price,	volume,	dividend_amount,	stock_split)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, [stock_id, date, row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], row['Dividends'], row['Stock Splits']])
    
    commit_and_close(connection)
    
    
    # with open("test.csv", 'w') as writer:
    #     history.to_csv(writer, index=True)
    # print(f"Downloaded {ticker}")
    # print(f"Stock history for {ticker} collected successfully")
    
    

    
    
if __name__ == "__main__":
    initialize_database()
    
    for stock in stocks_to_collect:
        collect_stock_history(stock)
    
    