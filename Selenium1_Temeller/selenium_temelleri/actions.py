from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

url = 'https://quotes.toscrape.com/js'

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
actions = ActionChains(driver)
driver.get(url)

next_button = driver.find_element(By.CSS_SELECTOR, 'li.next a')
actions.move_to_element(next_button).perform()
next_button.click()

