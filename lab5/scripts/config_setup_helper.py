import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')


import pymysql
import praw

from secrets_import import *



# Reddit API Authentication
reddit = praw.Reddit(
    client_id=config['reddit']['client_id'],
    client_secret=config['reddit']['client_secret'],
    user_agent=config['reddit']['user_agent']
)



def setup_database():
    """Ensure database and table exist before inserting data."""
    conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD) 
    cursor = conn.cursor()

    # Create database if it does not exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
    conn.select_db(MYSQL_DB)

    # Create table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title TEXT,
            content TEXT,
            timestamp DATETIME,
            subreddit VARCHAR(255),
            keywords TEXT,
            image_text TEXT,
            cluster_id INT,
            cluster_id_doc INT
        )
    """)

    conn.commit()
    conn.close()
    print("Database and table setup complete.")
    