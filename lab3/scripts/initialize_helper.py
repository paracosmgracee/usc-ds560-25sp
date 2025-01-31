from mysql_helper import *
import yfinance as yf


create_database_query = "CREATE DATABASE IF NOT EXISTS DSCI560_Stocks"

tables_queries = [
    """
    CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);""", 
"""
CREATE TABLE IF NOT EXISTS Stocks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    ticker VARCHAR(10) UNIQUE NOT NULL
);""", """

CREATE TABLE IF NOT EXISTS Portfolios (
    portfolio_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(Id)
);""", """

CREATE TABLE IF NOT EXISTS Portfolio_details (
    portfolio_id INT NOT NULL,
    stock_id INT NOT NULL,
    PRIMARY KEY (portfolio_id, stock_id),
    FOREIGN KEY (portfolio_id) REFERENCES Portfolios(portfolio_id),
    FOREIGN KEY (stock_id) REFERENCES Stocks(id)
);"""
]



def initialize_database():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(create_database_query)
    cursor.execute("USE DSCI560_Stocks")
    
    for query in tables_queries:
        cursor.execute(query)
    
    commit_and_close(connection)
    print("Database initialized successfully")
    
    
def validate_user(name, password=None):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM Users WHERE name = %s", [name])
    
    user = cursor.fetchone()
    
    
    if password:
        if user[2] == password:
            return user
        else:
            return None
        
    commit_and_close(connection)
    
    return user
    

def create_user(name, password):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO Users (name, password) VALUES (%s, %s)", (name, password))
    
    commit_and_close(connection)
    print("User created successfully")
    
    
def validate_portfolio(user_id, portfolio_name):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM Portfolios WHERE user_id = %s AND name = %s", (user_id, portfolio_name))
    
    portfolio = cursor.fetchone()
    
    commit_and_close(connection)
    
    return portfolio

def create_portfolio(user_id, portfolio_name):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO Portfolios (user_id, name) VALUES (%s, %s)", (user_id, portfolio_name))
    
    commit_and_close(connection)
    print("Portfolio created successfully")
    
def list_portfolios(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM Portfolios WHERE user_id = %s", [user_id])
    
    portfolios = cursor.fetchall()
    
    commit_and_close(connection)
    
    return portfolios
    

def list_stocks(user_id, portfolio_id):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM Portfolio_details p JOIN Stocks s ON (p.stock_id = s.id) WHERE p.portfolio_id = %s", [portfolio_id])
    
    stocks = cursor.fetchall()
    
    commit_and_close(connection)
    
    return stocks


def check_ticker(ticker):
    try:
        
        if yf.Ticker(ticker).info['shortName']:
            return yf.Ticker(ticker)
    except KeyError:
        print('Ticker not recognized')
        return None
    
def add_ticker(ticker, portfolio_id):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM Stocks WHERE ticker = %s", [ticker])
    
    stock = cursor.fetchone()
    
    
    name = check_ticker(ticker).info['shortName']
    
    if not stock:
        cursor.execute("INSERT INTO Stocks (name, ticker) VALUES (%s, %s)", (name, ticker))
        cursor.execute("SELECT * FROM Stocks WHERE ticker = %s", [ticker])
        stock = cursor.fetchone()
        
    cursor.execute("INSERT INTO Portfolio_details (portfolio_id, stock_id) VALUES (%s, %s)", (portfolio_id, stock[0]))
    
    commit_and_close(connection)
    print("Stock added successfully")
    
def delete_ticker_from_portfolio(portfolio_id, stock_id):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM Portfolio_details WHERE portfolio_id = %s AND stock_id = %s", (portfolio_id, stock_id))
    
    commit_and_close(connection)
    print("Stock deleted from portfolio successfully")
    
