# Laboratory Assignment 3

## Problem Statement 
This assignment focuses on providing you hands-on experience with building a real-time stock price 
analysis and algorithmic trading model. We will focus on data collection, storage, and pre-processing to get 
your team ready to perform analysis and algorithmic trading on the stored data. 
In this lab, you will work with your team to design and implement functions that would dynamically fetch 
stock data using the finance API. Additionally, you'll explore different ways to efficiently store and quickly 
retrieve the data from the database.  

## Video Demo Link
  TBD

## Technologies Used
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](#)
[![VMware Workstation Pro](https://img.shields.io/badge/VMware_Workstation_Pro-607078?style=for-the-badge&logo=vmware&logoColor=white)](#)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=fff)](#)


## How to run Application Locally
1. Clone the GitHub Project
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install python and the requirements
3. Initialize the Database using the initialize_helper.py script
3. Run the collect_stock_history, it will collect data and store it in the database

## Code details
1. **Initialize Database**: The `initialize_database` function in [`collect_stock_history.py`](Lab_3/scripts/collect_stock_history.py) creates the necessary tables in the MySQL database.
2. **Save Stock Info**: The `save_stock_info` function fetches stock information using the yFinance API and inserts or updates the stock details in the `Stocks_analysis` table.
3. **Collect Stock History**: The `collect_stock_history_func` function fetches historical stock data for specified periods and intervals, and inserts the data into the `stock_history` table.
4. **Save Table to CSV**: The `save_table_to_csv` function exports the contents of a specified database table to a CSV file.

## References

- [yFinance Documentation](https://pypi.org/project/yfinance/)
- [MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Readme File Template](https://www.readme-templates.com/)
