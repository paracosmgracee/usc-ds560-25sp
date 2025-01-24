import pandas as pd
from pdf_extraction_helpers import *
from html_extraction_helper import *
    
    

## Task: Extract structured data from a CSV file

def get_data_from_csv():
    #uploaded destinations.csv 
    #from https://www.kaggle.com/datasets/faizadani/european-tour-destinations-dataset?select=destinations.csv 
    #to Google Drive for easy access with new link
    df = pd.read_csv("https://drive.google.com/uc?id=1yXmfBxtt1RGJK0HImvcv3ZlTz97RWUcD", encoding='latin1')
    #display first few records
    print(df.head())

    #calculate size and dimension of datset
    print("size: ", df.size)
    print("dimension (row, col): ", df.shape)

    #identify missing data
    print("missing values present: ", df.isnull().values.any())
    print("missing values per col: ")
    print(df.isnull().sum())
    print("total missing values: ", df.isnull().sum().sum())
    
def get_data_from_pdf():
    # Defining the PDF file name and URL
    pdf_file = "LA_Tourist_Itinerary.pdf"
    url = "https://latourist.com/documents/LA_Tourist_Itinerary.pdf"

    # Downloading the raw PDF file from the URL
    get_raw_data_from_url(url, pdf_file)

    # Extracting text from the downloaded PDF file and save it to a text file
    extract_text_from_pdf(pdf_file, "LA_Tourist_Itinerary.txt")

    # Extracting structured data from the text file and create a DataFrame
    df = get_data_from_text("LA_Tourist_Itinerary.txt")

    # Saving the DataFrame to a CSV file
    save_to_csv(df, "Lab 2\\processed_data\\LA_Tourist_Itinerary.csv")

    # Printing the first few records of the DataFrame
    print("\nFirst few records:")
    print(df.head())

    # Printing the dimensions of the DataFrame
    print("\nDataset dimensions:")
    print(df.shape)

    # Checking for missing data in the DataFrame
    print("\nMissing data check:")
    print(df.isnull().sum())
    
def get_data_from_html():
    csv_path = scrape_cards()
    explore_dataset(csv_path)
    

if __name__ == "__main__":
    
    
    
    print("Extracting data from csv file")
    get_data_from_csv()
    
    print("\nExtracting data from pdf file")
    get_data_from_pdf()
    
    print("\nExtracting data from HTML file")
    get_data_from_html()