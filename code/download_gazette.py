import os
import sys
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from tqdm import tqdm


def download_file(session, file_url, output_dir):
        file_response = session.get(file_url, allow_redirects=True)
        filename = os.path.basename(file_response.url)
        file_destination = os.path.join(output_dir, filename)
        if not os.path.exists(file_destination):
            with open(file_destination, 'wb') as open_destination_file:
                open_destination_file.write(file_response.content)

def main(country_code):
    rel_out_path = os.path.join('data', country_code, 'pdfs')
    output_dir = os.path.abspath(rel_out_path)
    os.makedirs(output_dir, exist_ok=True)
    # Define the retry strategy
    retry_strategy = Retry(
        total=10,  # Maximum number of retries
        backoff_factor=2,  # Exponential backoff factor (e.g., 2 means 1, 2, 4, 8 seconds, ...)
        status_forcelist=[429, 500, 502, 503, 504],  # HTTP status codes to retry on
    )
    # Create an HTTP adapter with the retry strategy and mount it to session
    adapter = HTTPAdapter(max_retries=retry_strategy)

    # Create a new session object
    session = requests.Session()
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    base_url = 'https://gazettes.africa'
    country_url = '{}/gazettes/{}/'.format(base_url, country_code)
    country_response = session.get(country_url)
    country_soup = BeautifulSoup(country_response.content, 'html.parser')

    year_titles = country_soup.find_all('h2', 'fw-bold')
    for year_title in tqdm(year_titles):
        year_href = year_title.find('a').get('href')
        year_url = '{}{}'.format(base_url, year_href)

        year_response = session.get(year_url)
        year_soup = BeautifulSoup(year_response.content, 'html.parser')

        year_table = year_soup.find('table')
        gazette_anchors = year_table.find_all('a')
        for gazette_anchor in gazette_anchors:
            gazette_href = gazette_anchor.get('href')
            gazette_url = '{}{}'.format(base_url, gazette_href)
            gazette_response = session.get(gazette_url)
            gazette_soup = BeautifulSoup(gazette_response.content, 'html.parser')
            file_href = gazette_soup.find('a', 'btn-shrink-sm').get('href')
            file_url = '{}{}'.format(base_url, file_href)
            download_file(session, file_url, output_dir)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Enter country code as first positional argument.")
    else:
        main(sys.argv[1])