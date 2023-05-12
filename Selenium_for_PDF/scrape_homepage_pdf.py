import time
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from urllib.parse import urlparse
import logging
#from bs4 import BeautifulSoup
#import pandas
#import selenium
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#import re

def check_if_link_is_used(link, used_links):
    # Testet ob der Link schonmal aufgerufen wurde
    if link in used_links:
        True
    else:
        False

def belongs_to_homepage(link_url, homepage_url):
    # Testet ob der Link noch zur Homepage gehört oder nicht
    link_domain = urlparse(link_url).netloc
    homepage_domain = urlparse(homepage_url).netloc
    return (link_domain == homepage_domain)


def search_links(url, download_dir, driver, depth=0):
    # Alle Links auf der Seite abrufen
    wait = WebDriverWait(driver, 10)
    a_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
    print('A')
    print(a_elements)
    
    # Durch alle Links auf der Seite iterieren
    for link in a_elements:
        #print('B')
        # Besuchte Links sowie Links zu anderen Homepages überspringen
        if check_if_link_is_used(link, used_links) or not belongs_to_homepage(link, url):
            continue
        else:    
            used_links.add(link)
            href = link.get_attribute('href')
            if '.pdf' in href.lower():
                # PDF-Link gefunden, herunterladen
                filename = os.path.join(download_dir, href.split('/')[-1])
                print(link)
                link.click()
        
                # Explizit auf das Herunterladen warten, bis die Datei im Downloadverzeichnis erscheint
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{filename}')]")))
        
                # Datei in das gewünschte Verzeichnis verschieben
                downloaded_file = max([os.path.join(download_dir, f) for f in os.listdir(download_dir)], key=os.path.getctime)
                os.rename(downloaded_file, filename)
                print(f'{filename} heruntergeladen.')
            else:
                # Link verweist nicht auf PDF, rekursiv nach weiteren Links suchen
                search_links(href, download_dir, depth + 1)


def get_pdf_from_homepages(url_list):
    # Pfad zum Speichern der heruntergeladenen PDF-Dateien
    current_file_path = os.path.abspath(__file__)
    download_dir = os.path.dirname(current_file_path)

    # Start des Webdrivers (z.B. Chrome)
    # driver = webdriver.Chrome()

    # Create a new Firefox WebDriver instance
    firefox_options = Options()
    #firefox_options.headless = True
    geckodriver_path = str(download_dir) + '/geckodriver'
    print(geckodriver_path)
    service = Service(geckodriver_path)
    try:
        driver = webdriver.Firefox(service=service)
    except WebDriverException as e:
        print(f"WebDriverException occurred: {e}")
    logging.basicConfig(level=logging.DEBUG)
    

    # Impizite Wartezeit von 10 Sekunden festlegen
    driver.implicitly_wait(10)

    used_links = set()
    for url in url_list:
        # Downloads pdf
        search_links(url, download_dir, driver)

    # Webdriver beenden
    driver.quit()


if __name__ == "__main__":
    url_list = ['www.deutsche-bank.de', 'www.metzler.com']
    get_pdf_from_homepages(url_list)
