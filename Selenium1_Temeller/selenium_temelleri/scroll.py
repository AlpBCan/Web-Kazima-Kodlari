from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

def scroll_to_bottom():
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(1)

url = 'https://quotes.toscrape.com/scroll'

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
driver.get(url)

sleep(2)

old_height = driver.execute_script('return document.body.scrollHeight')

while True:
    scroll_to_bottom()
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == old_height:
        break
    old_height = new_height

quotes = driver.find_elements(By.CSS_SELECTOR, 'div.quote')
print(len(quotes))



