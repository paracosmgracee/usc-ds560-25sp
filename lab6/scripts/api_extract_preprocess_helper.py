import pymysql
import requests
from bs4 import BeautifulSoup
import re
from secrets_import import * 

TABLE_NAME = "oil_wells_information"

## needed
def connect_db():
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    
## needed    
def get_well_list_from_db():
    conn = connect_db()
    with conn.cursor() as cursor:
        query = f"SELECT api_number, well_name FROM {TABLE_NAME};"
        cursor.execute(query)
        well_list = cursor.fetchall()
    conn.close()
    return well_list

## needed
def check_and_create_columns():
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute(f"SHOW COLUMNS FROM {TABLE_NAME};")
        existing_columns = {row["Field"] for row in cursor.fetchall()}
        required_columns = {
            "well_status": "VARCHAR(50)",
            "well_type": "VARCHAR(50)",
            "closest_city": "VARCHAR(50)",
            "barrels_of_oil_produced": "VARCHAR(50)",
            "mcf_of_gas_produced": "VARCHAR(50)",
        }
        for column, data_type in required_columns.items():
            if column not in existing_columns:
                alter_query = f"ALTER TABLE {TABLE_NAME} ADD COLUMN {column} {data_type};"
                cursor.execute(alter_query)
                print(f"Created new column: {column}")
    conn.commit()
    conn.close()
    
def clean_text(text):
    if text is None:
        return "N/A"
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s,.%-]', '', text)
    return text.strip()

def clean_numeric(value):
    if value is None or value == "" or value.lower() == "n/a":
        return 0
    value = value.replace(",", "")
    value = re.sub(r'[^\d.]', '', value)
    try:
        return int(value) if "." not in value else float(value)
    except ValueError:
        return 0

def get_data_by_th(soup, th_text):
    th = soup.find("th", string=th_text)
    if th and th.next_sibling:
        return th.next_sibling.get_text(strip=True)
    return None


def get_well_details(well_name=None, api_number=None):
    DRILLING_EDGE_BASE_SEARCH_URL = "https://www.drillingedge.com/search"
    params = {"type": "wells"}
    if well_name:
        params["well_name"] = well_name
    if api_number:
        params["api_number"] = api_number

    results = {
        "api_number": api_number,
        "well_name": well_name,
        "well_status": "N/A",
        "well_type": "N/A",
        "closest_city": "N/A",
        "barrels_of_oil_produced": 0,
        "mcf_of_gas_produced": 0,
    }
    response = requests.get(DRILLING_EDGE_BASE_SEARCH_URL, params=params)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        well_page_links = soup.find("table", class_="table wide-table interest_table")
        if not well_page_links:
            print(f"No well search results found: {well_name} / {api_number}")
            return results
        well_page_link_tag = well_page_links.find("a")
        if well_page_link_tag and "href" in well_page_link_tag.attrs:
            well_page_link = well_page_link_tag["href"]
        else:
            print(f"No detail page link found: {well_name} / {api_number}")
            return results
        response = requests.get(well_page_link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            results["well_status"] = clean_text(get_data_by_th(soup, "Well Status"))
            results["well_type"] = clean_text(get_data_by_th(soup, "Well Type"))
            results["closest_city"] = clean_text(get_data_by_th(soup, "Closest City"))

            production_stats = soup.find_all("p", class_="block_stat")
            for stat in production_stats:
                span_value = stat.find("span", class_="dropcap")
                if span_value:
                    value = span_value.text.strip()

                    if "Barrels of Oil Produced" in stat.text:
                        results["barrels_of_oil_produced"] = clean_numeric(value)
                    elif "MCF of Gas Produced" in stat.text:
                        results["mcf_of_gas_produced"] = clean_numeric(value)
    return results
