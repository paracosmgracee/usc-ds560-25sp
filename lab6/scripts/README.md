# Laboratory Assignment 6

## Problem Statement 
This assignment focuses on web scraping, data preprocessing, data analysis, clustering algorithms, and real-time data processing. You will better understand how to collect and organize data from online forums and create a system for clustering related documents. When you review the document contents, you will find 
that many are irrelevant, misleading, and/or undesirable. You will need to use reasonable methods to clean the data set before you store it in a database.

## Video Demo Link
  TBD

## Technologies Used
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](#)
[![VMware Workstation Pro](https://img.shields.io/badge/VMware_Workstation_Pro-607078?style=for-the-badge&logo=vmware&logoColor=white)](#)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=fff)](#)
[![PyMuPDF](https://img.shields.io/badge/PyMuPDF-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://pymupdf.readthedocs.io/)
[![Tesseract](https://img.shields.io/badge/Tesseract-FF6F00?style=for-the-badge&logo=tesseract&logoColor=white)](https://github.com/tesseract-ocr/tesseract)
[![ThreadPoolExecutor](https://img.shields.io/badge/ThreadPoolExecutor-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor)
[![ProcessPoolExecutor](https://img.shields.io/badge/ProcessPoolExecutor-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor)

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
4. Run the `scrape_pdf.py` script to extract data from PDFs
   ```sh
   python scrape_pdf.py
   ```
5. Run the `extract_data_text.ipynb` notebook to process the extracted text data
   ```sh
   jupyter notebook extract_data_text.ipynb
   ```
6. Run the `api_extract_preprocess_multithreading.py` script to extract and preprocess well data
   ```sh
   python api_extract_preprocess_multithreading.py
   ```

## Code details
1. **Extract Data from PDFs**: The `scrape_pdf.py` script extracts data from PDF files and processes them.
2. **Extract and Process Text Data**: The `extract_data_text.ipynb` notebook extracts and processes text data from the PDFs and writes the results to the database.
3. **Database Operations**: The `secrets_import.py` script contains the database connection details and helper functions for database operations.
4. **Multithreading for API Extraction**: The `api_extract_preprocess_multithreading.py` script uses multithreading to extract and preprocess well data from APIs.
5. **Helper Functions**: The `api_extract_preprocess_helper.py` script contains helper functions for connecting to the database, cleaning data, and extracting well details.

## References

- [MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/)
- [NLTK Documentation](https://www.nltk.org/)
- [Gensim Documentation](https://radimrehurek.com/gensim/)
- [Pytesseract Documentation](https://pypi.org/project/pytesseract/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [ThreadPoolExecutor Documentation](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor)
- [ProcessPoolExecutor Documentation](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://docs.python-requests.org/en/latest/)
