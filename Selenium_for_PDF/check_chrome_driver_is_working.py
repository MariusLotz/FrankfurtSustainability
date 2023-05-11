from selenium import webdriver

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Check if WebDriver is working
if driver.title:
    print("Chrome WebDriver is working.")
else:
    print("Chrome WebDriver is not working.")

# Quit the WebDriver
driver.quit()