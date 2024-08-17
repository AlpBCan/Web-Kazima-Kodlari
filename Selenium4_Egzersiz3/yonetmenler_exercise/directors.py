'''
    Sıra sizde!!!

    Drama kategorisinde 'Best Director' ödülünü alan yönetmenleri bulup boylarını kaydedeceksiniz :)

    Bu linkten başlayın:
    https://www.imdb.com/search/title/

'''


# Gerekli kütüphaneleri import edin, eğer ihtiyaç olursa sonradan de eklemeler yapabilirsiniz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pandas as pd
import openpyxl


# Veriyi kaydetmek için bir dictionary oluşturun. Key'ler: 'name', 'height'
directors_dict = {'name': [], 'height': []}


# Option'ları tanımlayın, driver'ı oluşturun, ana sayfayı driver ile açın
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
actions = ActionChains(driver)
driver.get('https://www.imdb.com/search/title/')


# Cookie tercihini kontrol edin eğer belirirse kabul edin
try:
    accept_button = driver.find_element(By.XPATH, '//button[text()="Accept"]')
    accept_button.click()
except:
    pass


# Genre'dan Drama kategorisini seçin ve Awards & Recognition'dan 'Best Director-Winning'i seçin,
# See results'a tıklayın

sleep(1)

genre = driver.find_element(By.XPATH, '//div[text()="Genre"]')
actions.move_to_element(genre).perform()
genre.click()

sleep(1)

drama_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-Drama"]')
actions.move_to_element(drama_button).perform()
drama_button.click()

sleep(1)

awards_button = driver.find_element(By.XPATH, '//div[text()="Awards & recognition"]')
actions.move_to_element(awards_button).perform()
awards_button.click()

sleep(1)

director_winning_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-best-director-winning"]')
actions.move_to_element(director_winning_button).perform()
director_winning_button.click()

sleep(1)

results_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="See results"]')
actions.move_to_element(results_button).perform()
results_button.click()


# Aşağıdaki 'more' butonuna basarak tüm filmleri yüklemek için bir loop oluşturun
while True:
    sleep(2)
    more_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.ipc-see-more__text')
    if len(more_buttons) != 0:
        more_button = more_buttons[0]
        actions.move_to_element(more_button).perform()
        more_button.click()
    else:
        break


# Filmlerin sağ tarafındaki info butonlarının(svg etiketini kullanın) listesini alın
i_buttons = driver.find_elements(By.CSS_SELECTOR, 'svg.ipc-icon--info')


# Bu info butonlarına tek tek tıklamak için bir loop oluşturun ve bunlardan yönetmenlerin linklerini alıp
# bir listeye koyun
directors_list = []
for i_button in i_buttons:
    actions.move_to_element(i_button).perform()
    i_button.click()
    sleep(0.5)
    a_tag = driver.find_element(By.CSS_SELECTOR, 'a.gryEiE')
    link = a_tag.get_attribute('href')
    directors_list.append(link)
    close_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close Prompt"]')
    actions.move_to_element(close_button).perform()
    close_button.click()
    sleep(0.5)


# Başka bir loop ile tüm yönetmen linklerini ziyaret edin, isimlerini ve boylarını(eğer sayfada varsa) başta
# oluşturduğunuz dictionary'e kaydedin
for link in directors_list:
    driver.get(link)

    try:
        name = driver.find_element(By.CSS_SELECTOR, 'h1[data-testid="hero__pageTitle"] span[data-testid="hero__primary-text"]').text
    except:
        name = 'Bilgi yok'

    try:
        height = driver.find_element(By.XPATH, '//span[text()="Height"]/following-sibling::div[1]/ul/li/span').text
    except:
        height = 'Bilgi yok'

    directors_dict['name'].append(name)
    print(name)
    directors_dict['height'].append(height)
    print(height)



# Pandas kullanarak verileri Excel dosyası olarak kaydedin
df = pd.DataFrame(directors_dict)
df.to_excel('boylar.xlsx')


