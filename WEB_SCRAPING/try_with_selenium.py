from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    # Configure Selenium options
    options = Options()
    options.headless = True  # Run the browser in headless mode (without UI)

    # Set path to chromedriver executable
    chromedriver_path = '/home/user/Coding/chromedriver'

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

    try:
        # Open Google homepage
        driver.get("https://www.google.com")

        # Find the search input field
        search_input = driver.find_element(By.NAME, "q")

        # Enter the search query
        search_query = "banks in Frankfurt"
        search_input.send_keys(search_query)

        # Perform the search
        search_input.send_keys(Keys.RETURN)

        # Find the search results
        search_results = driver.find_elements(By.XPATH, "//div[@class='g']")

        # Extract relevant information from the search results
        for result in search_results:
            title = result.find_element(By.XPATH, ".//h3").text
            link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
            print(f"Title: {title}")
            print(f"Link: {link}")
            print("---")

    finally:
        # Quit the driver
        driver.quit()

if __name__ == "__main__":
    main()