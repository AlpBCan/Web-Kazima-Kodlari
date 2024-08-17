from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pandas as pd
import openpyxl

movie_dict = {
    'name': [],
    'year': [],
    'duration': [],
    'stars': [],
    'votes': [],
    'metascore': [],
    'description': []
}

def accept_cookies(the_driver):
    try:
        accept_cookies = the_driver.find_element(By.XPATH, '//button[text()="Accept"]')
        accept_cookies.click()
    except:
        pass


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
actions = ActionChains(driver)
driver.implicitly_wait(1)

driver.get('https://www.imdb.com/')

sleep(2)

accept_cookies(driver)

sleep(1)

search_button = driver.find_element(By.ID, 'suggestion-search-button')
search_button.click()

sleep(1)

movies_tv = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="advanced-search-chip-tt"]')
movies_tv.click()

sleep(1)

title_type = driver.find_element(By.XPATH, '//div[text()="Title type"]')
actions.move_to_element(title_type).perform()
title_type.click()

sleep(1)

movie = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-movie"]')
actions.move_to_element(movie).perform()
movie.click()

sleep(1)

genre = driver.find_element(By.XPATH, '//div[text()="Genre"]')
actions.move_to_element(genre).perform()
genre.click()

sleep(1)

comedy = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-Comedy"]')
actions.move_to_element(comedy).perform()
comedy.click()

sleep(1)
# Awards & recognition
awards = driver.find_element(By.XPATH, '//div[text()="Awards & recognition"]')
actions.move_to_element(awards).perform()
awards.click()

sleep(1)

oscar_nom = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-oscar-nominated"]')
actions.move_to_element(oscar_nom).perform()
oscar_nom.click()

sleep(1)

results_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="See results"]')
driver.execute_script('arguments[0].click()', results_button)

while True:
    sleep(2)
    more_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.ipc-see-more__text')
    if len(more_buttons) != 0:
        more_button = more_buttons[0]
        actions.move_to_element(more_button).perform()
        more_button.click()
    else:
        break

movies = driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item')

for movie in movies:
    # 1. Inside Out
    raw_name = movie.find_element(By.CSS_SELECTOR, 'h3.ipc-title__text').text
    name = ' '.join(raw_name.split(' ')[1:])
    print(name)
    movie_dict['name'].append(name)

    year = movie.find_elements(By.CSS_SELECTOR, 'span.dli-title-metadata-item')[0].text
    print(year)
    movie_dict['year'].append(year)

    duration = movie.find_elements(By.CSS_SELECTOR, 'span.dli-title-metadata-item')[1].text
    print(duration)
    movie_dict['duration'].append(duration)

    stars = movie.find_element(By.CSS_SELECTOR, 'span.ipc-rating-star--rating').text
    print(stars)
    movie_dict['stars'].append(stars)

    # (818K)
    votes = movie.find_element(By.CLASS_NAME, 'ipc-rating-star--voteCount').text.strip()[1:-1]
    print(votes)
    movie_dict['votes'].append(votes)

    try:
        metascore = movie.find_element(By.CSS_SELECTOR, 'span.metacritic-score-box').text
    except:
        metascore = 'Bilgi yok'

    print(metascore)
    movie_dict['metascore'].append(metascore)

    description = movie.find_element(By.CSS_SELECTOR, 'div.ipc-html-content-inner-div').text
    print(description)
    movie_dict['description'].append(description)
    print('\n')

df = pd.DataFrame(movie_dict)
df.to_excel('filmler.xlsx')



