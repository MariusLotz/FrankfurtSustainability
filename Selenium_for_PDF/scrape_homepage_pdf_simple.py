import time
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import logging
import re

def check_if_link_is_used(link, used_links):
    # Testing if link was already called
    if link in used_links:
        True
    else:
        False

def belongs_to_homepage(link_url, homepage_url):
    # Testing if link belongs to main homepage or refers to another site
    link_domain = urlparse(link_url).netloc
    homepage_domain = urlparse(homepage_url).netloc
    return (link_domain == homepage_domain) # todo: anpassen nicht so restriktiv


def find_new_links(url, homepage, used_links, driver):
    # Open a webpage
    driver.get(url)
    used_links.add(url)
    time.sleep(1)  # Wait for 1 seconds

    # Find all link elements
    links=[]
    a_elements = driver.find_elements(By.TAG_NAME, "a")
    for a_element in a_elements:
        link = a_element.get_attribute('href')
        if link in used_links:
            continue
        elif not belongs_to_homepage(link, homepage):
            continue
        else:
            links.append(link)
    return links
    

def search_links(homepage, link, used_links, driver):
    links = find_new_links(link, homepage, used_links, driver)
    #print(links[0:5])
    
    # Iterate trough all all found links:
    temp_links = []
    for link in links:
        print(link)
        used_links.add(link)
        if '.pdf' in link.lower():
            print('pdf found')
            # PDF-Link gefunden, herunterladen
            #filename = os.path.join(download_dir, link.split('/')[-1])
            driver.get(link)
    
            # Datei in das gewünschte Verzeichnis verschieben
            #downloaded_file = max([os.path.join(download_dir, f) for f in os.listdir(download_dir)], key=os.path.getctime)
            #os.rename(downloaded_file, filename)
            #print(f'{filename} heruntergeladen.')
        else:
            print('no pdf, go to next link')
            # Link verweist nicht auf PDF, rekursiv nach weiteren Links suchen
            temp_links.append(link)
    for link in temp_links:        
        search_links(homepage, link, used_links, driver)
            


def get_pdf_from_homepages(url_list):
    # Pfad zum Speichern der heruntergeladenen PDF-Dateien
    current_file_path = os.path.abspath(__file__)
    download_dir = os.path.dirname(current_file_path)

    # Start des Webdrivers (z.B. Chrome)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option(
    "prefs", {"download.default_directory": str(download_dir) + '/scraped_pdf'})
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(2)  # Wait for 2 seconds
    #logging.basicConfig(level=logging.DEBUG)
    
    # Start scraping
    used_links = set()
    for homepage in url_list:
        # Downloads pdf
        used_links.add(homepage)
        search_links(homepage, homepage, used_links, driver)

    # Webdriver beenden
    driver.quit()


if __name__ == "__main__":
    url_list = ['https://www.metzler.com/de/metzler']
    url_list1 = ['https://www.db.com/']
    get_pdf_from_homepages(url_list1)
