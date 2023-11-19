import os # For file and directory operations.

# Python library for making HTTP requests. 
# It is used here to send GET requests to the webpage and download the content.
import requests

# For web scraping and parsing HTML content.
# It helps in navigating and searching the HTML tree structure.
from bs4 import BeautifulSoup

# From Python standard library
# Construct absolute URLs from base URL and relative URLs
''' 
DEF Base URL: starting point or the foundation of a URL. 
    It includes the scheme (such as "http" or "https"), 
    the domain (like "www.example.com"), and any initial path information.
    For example, in the URL "https://www.example.com/page/index.html", 
    the base URL is "https://www.example.com".
EX Relative URLs
    `/images/picture.jpg` (points to an image in the "images" directory 
        on the same domain)
    `../page2.html` (points to a page one level up in the directory structure)
Constructing absolute URLs involves combining a base URL and a 
    relative URL to create a complete and valid URL.
'''
from urllib.parse import urljoin

# Downloads all the txt files present in url and put them in download_folder
def download_text_files(url, download_folder):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the links (a tags) in the HTML and put them in a list
        links = soup.find_all('a')

        # Create the download folder if it doesn't exist
        os.makedirs(download_folder, exist_ok=True)

        # For every downloadable files present...
        for link in links:
            # Get the href attribute from the link
            href = link.get('href')

            # Check if the link ends with '.txt'
            if href and href.endswith('.txt'):
                # Build the absolute URL
                absolute_url = urljoin(url, href)

                # Get the text file name from the URL
                file_name = os.path.join(download_folder, os.path.basename(href))

                # Download the file
                '''with statement is used here to ensure that the file is
                    properly closed after writing, even if an error occurs 
                    during the process'''
                with open(file_name, 'wb') as file:
                    file_content = requests.get(absolute_url).content
                    file.write(file_content)
                    print(f"Downloaded: {file_name}")
                    
        print(f"Download completed for {url}. Files saved in {download_folder}")

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

'''
# Specify the URL of the webpage and the folder to save the downloaded files
webpage_url = 'http://www.textfiles.com/politics/CIA/'
download_folder = 'downloaded_files'

# Call the function to download text files
download_text_files(webpage_url, download_folder)
'''