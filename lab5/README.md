# Laboratory Assignment 5

## Problem Statement 
This assignment focuses on web scraping, data preprocessing, data analysis, clustering algorithms, and real-time data processing. You will better understand how to collect and organize data from online forums and create a system for clustering related documents. When you review the document contents, you will find that many are irrelevant, misleading, and/or undesirable. You will need to use reasonable methods to clean the data set before you store it in a database.

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
   ```sh
   pip install -r requirements.txt
   ```
3. Initialize the Database using the `initialize_helper.py` script
   ```sh
   python initialize_helper.py
   ```
4. Run the `automate.py` script to start the automation process
   ```sh
   python automate.py 5
   ```

## Code details
1. **Fetch and Store Reddit Posts**: The `fetch_and_store_reddit_posts` function in [`reddit_scraper.py`](reddit_scraper.py) fetches posts from a specified subreddit and stores them in the database.
2. **Generate Embeddings**: The `generate_embeddings` function generates Doc2Vec and Word2Vec embeddings for the posts.
3. **Cluster Messages**: The `cluster_messages` function clusters the posts using KMeans clustering.
4. **Find Similar Posts**: The `find_similar_posts` function finds and displays posts similar to a given query.

## References

- [MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/)
- [NLTK Documentation](https://www.nltk.org/)
- [Gensim Documentation](https://radimrehurek.com/gensim/)
- [Pytesseract Documentation](https://pypi.org/project/pytesseract/)
