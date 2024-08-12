# -*- coding=utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path: str = "./chromedriver-win64/chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_services = webdriver.ChromeService(executable_path=chromedriver_path)
chrome_options.binary_location = "./chrome-win64/chrome.exe"
# Initialize the WebDriver
with webdriver.Chrome(options=chrome_options, service=chrome_services) as driver:
    # Open the target URL
    url = "https://www.taiwanlottery.com/lotto/result/super_lotto638/"
    driver.get(url)

    # Wait for the AJAX content to load
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="__nuxt"]/main/div[2]/div/div[1]/aside/div')
        )
    )
    # Interact with the AJAX-loaded content
    print(element.text.replace("\n", ""))
    # driver.quit()
