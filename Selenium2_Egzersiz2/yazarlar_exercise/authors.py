'''
    Sıra sizde!!!

    Selenium kullarak aşağıdaki verileri bir excel dosyasına kaydedin:
        yazar ismi
        yazarın doğum tarihi
        yazarın doğum yeri

    Lütfen kendiniz yapmaya çalışın. Eğer takıldığınız bir yer olursa,
    çözüm videosundan sadece o kısma bakıp kodunuza geri dönün. Bol şans.

    url = https://quotes.toscrape.com/  -->  JS versiyonu olmayacak.

'''

# Gerekli kütüphaneleri import edin, eğer ihtiyaç olursa sonradan de eklemeler yapabilirsiniz.
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import openpyxl


# Veriyi kaydetmek için bir dictionary oluşturun
author_dict = {'name': [], 'birth_date': [], 'birth_place': []}


# Yazar sayfalarının linklerini kaydemek için boş bir liste oluşturun.
author_urls = []


# Option'ları tanımlayın, driver'ı oluşturun, ana sayfayı driver ile açın
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
driver.get('https://quotes.toscrape.com/')

# Login (Önceden beraber yaptığımızın aynısı)
login_button = driver.find_element(By.XPATH, '//a[text()="Login"]')
login_button.click()

username_input = driver.find_element(By.ID, 'username')
password_input = driver.find_element(By.ID, 'password')

username_input.send_keys('abcabc')
password_input.send_keys('123123')

login = driver.find_element(By.CSS_SELECTOR, 'input[value="Login"]')
login.click()


# Tüm sayfaları ziyaret etmek için bir loop oluşturun (Önceden beraber yaptığımızın aynısı)
# Bu loop ile tüm yazarların linklerini bulun((about) kısmından) ve önceden oluşturduğunuz boş listeye ekleyin
while True:
    quotes = driver.find_elements(By.CLASS_NAME, 'quote')
    for quote in quotes:
        author_link = quote.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        author_urls.append(author_link)
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'li.next a')
        next_button.click()
    except:
        break

# Yazar linkerinin listesini alın ve çiftleri elemek için bir setin içine koyun
author_urls = list(set(author_urls))


# Elde ettiğiniz yeni liste için yeni bir loop oluşturun ve bununla bütün yazar sayfalarını ziyaret ederek
# isim, doğum tarihi ve doğum yerini elde edip bunları dictionary'e ekleyin.
for url in author_urls:
    driver.get(url)
    name = driver.find_element(By.CSS_SELECTOR, 'h3.author-title').text
    author_dict['name'].append(name)

    birth_date = driver.find_element(By.CSS_SELECTOR, 'span.author-born-date').text
    author_dict['birth_date'].append(birth_date)

    birth_place = driver.find_element(By.CSS_SELECTOR, 'span.author-born-location').text
    author_dict['birth_place'].append(birth_place)

# Bir Pandas dataframe oluşturun, dictionary'i bunun içine koyun ve sonunda excel dosyası olarak verileri kaydedin
df = pd.DataFrame(author_dict)
df.to_excel('yazarlar.xlsx')