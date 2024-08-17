import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

with open('image_links.txt', 'w') as f:
    pass

book_dict = {
    'name': [],
    'price': [],
    'category': [],
    'stars': [],
    'upc': [],
    'availability': [],
    'in_stock': [],
    'image_link': []
}

number_dict = {'One': '1', 'Two': '2', 'Three': '3', 'Four': '4', 'Five': '5'}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

url = 'https://books.toscrape.com/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

page_count_string = soup.find('li', class_='current').text
page_count = int(page_count_string.strip().split(' ')[-1])

for page in range(1, page_count + 1):
    print('***********************************************')
    print(f'page -->  {page}')
    print('***********************************************')
    page_url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    response = requests.get(page_url)
    page_html = response.text
    soup = BeautifulSoup(page_html, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    for book in books:
        book_url = 'https://books.toscrape.com/catalogue/' + book.find('a')['href']
        response = requests.get(book_url, headers=headers)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')

        name = soup.find('div', class_='product_main').h1.text
        book_dict['name'].append(name)

        price = soup.find('div', class_='product_main').p.text
        book_dict['price'].append(price)

        ul_container = soup.find('ul', class_='breadcrumb')
        li_items = ul_container.find_all('li')
        category = li_items[2].a.text
        book_dict['category'].append(category)

        star_p_element = soup.find('p', class_='star-rating')
        star_class_name_list = star_p_element['class']
        star_string = star_class_name_list[1]
        stars = number_dict[star_string]
        book_dict['stars'].append(stars)

        upc_th = soup.find('th', string='UPC')
        upc = upc_th.find_next_sibling().text
        book_dict['upc'].append(upc)

        availability_th = soup.find('th', string='Availability')
        availability = availability_th.find_next_sibling().text
        book_dict['availability'].append(availability)

        # In stock (22 available)
        # 22 available)
        in_stock = availability.split('(')[1].split(' ')[0]
        book_dict['in_stock'].append(in_stock)

        image_link = 'https://books.toscrape.com/' + soup.find('div', class_='thumbnail').img['src'][6:]
        book_dict['image_link'].append(image_link)
        with open('image_links.txt', 'a') as f:
            f.write(image_link + '\n')



df = pd.DataFrame(book_dict)
df.to_excel('kitap.xlsx')


