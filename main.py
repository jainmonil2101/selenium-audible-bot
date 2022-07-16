from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time

options = Options()
options.headless = True
options.add_argument('window-size=1920x1080')

website = "https://www.audible.in/adblbestsellers"
path = 'chromedriver.exe'
driver = webdriver.Chrome(path, options=options)
driver.get(website)

# Pagination

pagination = driver.find_element_by_xpath(
    '//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements_by_tag_name('li')
last_page = int(pages[-2].text)

book_title = []
book_author = []
book_length = []

for i in range(1, last_page+1):
    driver.get(f"{website}?page={i}")


    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container ')))
    # container = driver.find_element_by_class_name('adbl-impression-container ')
    products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, './li')))
    # products = container.find_elements_by_xpath('./li')

    for product in products:
        book_title.append(product.find_element_by_xpath(
            './/h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element_by_xpath(
            './/li[contains(@class, "authorLabel")]/span/a').text)
        book_length.append(product.find_element_by_xpath(
            './/li[contains(@class, "runtimeLabel")]').text)
    

    
driver.quit()

df = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df.to_csv('book.csv', index=False)
