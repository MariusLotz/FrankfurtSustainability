import time
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
#from bs4 import BeautifulSoup
#import pandas
#import selenium
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#import re


used_links = set()

def check_if_link_is_used(link, used_links):
    # Testet ob der Link schonmal aufgerufen wurde
    if link is in used_links:
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
    a_elements = driver.find_elements(By.TAG_NAME, 'a')

    # Durch alle Links auf der Seite iterieren
    for link in a_elements:
        # Besuchte Links sowie Links zu anderen Homepages überspringen
        if check_if_link_is_used(link, used_links) or !belongs_to_homepage(link, url):
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


def get_pdf_from_homepages(url_list)
   
    # Start des Webdrivers (z.B. Chrome)
    driver = webdriver.Chrome()

    # Impizite Wartezeit von 10 Sekunden festlegen
    driver.implicitly_wait(10)

    # Pfad zum Speichern der heruntergeladenen PDF-Dateien
    current_file_path = os.path.abspath(__file__)
    download_dir = os.path.dirname(current_file_path)
  
    for url in url_list:
        # Downloads pdf_
        search_links(url, download_dir, driver)
    
    # Webdriver beenden
    driver.quit()


if __name__ == "__main__":
    url_list = ['https://www.deutsche-bank.de/']
    get_pdf_from_homepage()
