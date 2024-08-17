# name, price, category, stars, upc, availability, in_stock, image_link
import requests
from bs4 import BeautifulSoup

number_dict = {'One': '1', 'Two': '2', 'Three': '3', 'Four': '4', 'Five': '5'}

book_url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

response = requests.get(book_url)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, 'html.parser')

name = soup.find('div', class_='product_main').h1.text
print(name)

price = soup.find('div', class_='product_main').p.text
print(price)

ul_container = soup.find('ul', class_='breadcrumb')
li_items = ul_container.find_all('li')
category = li_items[2].a.text
print(category)

star_p_element = soup.find('p', class_='star-rating')
star_class_name_list = star_p_element['class']
star_string = star_class_name_list[1]
stars = number_dict[star_string]
print(stars)


upc_th = soup.find('th', string='UPC')
upc = upc_th.find_next_sibling().text
print(upc)

availability_th = soup.find('th', string='Availability')
availability = availability_th.find_next_sibling().text
print(availability)

# In stock (22 available)
# 22 available)
in_stock = availability.split('(')[1].split(' ')[0]
print(in_stock)

image_link = 'https://books.toscrape.com/' + soup.find('div', class_='thumbnail').img['src'][6:]
print(image_link)