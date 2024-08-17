import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

laptop_dict = {
    'name': [],
    'price': [],
    'shipping': [],
    'link': []
}

url = 'https://www.ebay.com/sch/i.html?_dcat=177&_fsrp=1&rt=nc&_from=R40&RAM%2520Size=32%2520GB&_nkw=laptop&_sacat=0&SSD%2520Capacity=1%2520TB'

#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

cookies = {
    'AMP_MKTG_f93443b04c': 'JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE',
    'AMP_f93443b04c': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIyYTMwYTgwMi1mYmMwLTRlNjctOWRkYi0zZTBmZGQ2YmFmZTklMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzIyOTMyMzMyODE4JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcyMjkzODAxMjk0MCUyQyUyMmxhc3RFdmVudElkJTIyJTNBMjExJTJDJTIycGFnZUNvdW50ZXIlMjIlM0ExMDIlN0Q=',
    'IDE': 'AHWqTUm78zrF1A-ODxAAdcRME1ek4Ae1li4n2np4tgwZpkCQjG7bI8m551gBJT1-Me8',
    '__deba': 'nBi0aQ0FNV9eNyjxNpJry_i1PSIK4b0oTo7HdwVYm8YYLO36mWqJ0wv3hJAl7K-AXR8UW1J2_XMwSXzXGqPFGIdaSpKUKkZ1OEGgI2fui4q2SvQVdo4ptTQJxz2Th-nEdoGErClX1eYaGZCeZLdvBQ==',
    '__gsas': 'ID=0bcec516fa4bb0e4:T=1722904546:RT=1722904546:S=ALNI_MYwYX3N8UxwbuWeHzD_LnSaT6watw',
    '__ssds': '2',
    '__ssuzjsr2': 'a9be0cd8e',
    '__uzma': 'ca1902fb-501a-4fa0-b9ca-434ef3061faa',
    '__uzmb': '1722904488',
    '__uzmc': '8896526259306',
    '__uzmd': '1722937622',
    '__uzme': '3141',
    '__uzmf': '7f60005ae2f453-77ec-4b5f-aa3e-ca50e7306e58172290448834333134124-dc132ac147103698262',
    'ak_bmsc': 'B515C0EF805DEEEAB7040B09F6DF8819~000000000000000000000000000000~YAAQjKDeUsRW2f6QAQAAqkvHJhjxxPpsvWsIkks7x/sUxzvzu6n5tPSXdnKwgM5yxi43XmgdMljk+2DkLHjrVREk7TOWN+EiEUQyE0lcTJn+9LjNoocA11jHiy7LIhEe3c6hecYIA6K+m/IXZycCdpUtSqE1u3hh2EKWSdEqKRMUmQ8evDfw9kXHSutekqVWdBqPNauLcEcv8Djgd/732FlDRfAi38UytvfPZaqE41d/Dq/YCrVOC1nHHI4Ft+D0FB9Twgnec6wWmMx/oUjWZvRmYiP7KLefVDmCEnz39P7Eyf/k9pyVsXWnWRB2wvFQeviEnaL7HZ/DOh0bYIvxF8xfVD5YNIKxRAuFJa7qBFcPO9EaNN5agxGHzWn7HC5ORqVgaK1VgBzGvw==',
    'ar_debug': '1',
    'bm_sv': '20B822CFD489DA65CF32F60B4A0CD4B3~YAAQjKDeUpwu2/6QAQAAfWMWJxikB7xCHWsYbTQ5waavu/S5+ftHVebE51RTgXPoeSs9r+gn0TQhMf7Ogm4oaR5F995har3FdkEVv6upWt30+SlhMeUuSOHS3ffEtRB3X/fU0ou34vxnaIKSgD4XZz4dlmdwqWDfHc9dEWkFlo9u8arjQBbxkc9JRZRqnpmR0cT+GYj+wDB81n01UNmVMi4O8PRXJAELQnuZqqeep2UNWSwG9bsspJRSkR9TJewq~1',
    'dp1': 'bu1p/QEBfX0BAX19AQA**6a74598b^pbf/%23e0002000000000000000006893260b^bl/US6a74598b^',
    'ebay': '%5Ejs%3D1%5Esbf%3D%23000000%5E',
    'nonsession': 'BAQAAAZBR14g6AAaAADMABWiTJgs5NDA0MwDKACBqdFmLMjUxYzIxZjkxOTEwYThjYzkzZGY5NTZmZmZmZjhjODUAywADZrH5kzIyMiYy4xksiQnVH3Gt9ysL/iaaOaW7',
    'ns1': 'BAQAAAZBR14g6AAaAANgAU2iTJgtjNjl8NjAxXjE3MjI5MDQ0OTA4NzVeXjFeM3wyfDV8NHw3fDEwfDQyfDQzfDExXl5eNF4zXjEyXjEyXjJeMV4xXjBeMV4wXjFeNjQ0MjQ1OTA3NdvgDCuqvBmsXMCOtURzCcwh2QzQ',
    's': 'CgADuAIpms0LAMwZodHRwczovL3d3dy5lYmF5LmNvbS9zY2gvaS5odG1sP19kY2F0PTE3NyZfZnNycD0xJnJ0PW5jJl9mcm9tPVI0MCZSQU0lMjUyMFNpemU9MzIlMjUyMEdCJl9ua3c9bGFwdG9wJl9zYWNhdD0wJlNTRCUyNTIwQ2FwYWNpdHk9MSUyNTIwVEIHAPgAIGazQsAyNTFjMjFmOTE5MTBhOGNjOTNkZjk1NmZmZmZmOGM4NYY3x6I*',

}

page_no = 1
while True:
    url = f'https://www.ebay.com/sch/i.html?_dcat=177&_fsrp=1&_from=R40&RAM%2520Size=32%2520GB&_nkw=laptop&_sacat=0&SSD%2520Capacity=1%2520TB&_pgn={page_no}&rt=nc'
    response = requests.get(url, headers=headers, cookies=cookies)
    print(response.status_code)
    if response.status_code != 200:
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    container = soup.find('div', attrs={'id': 'srp-river-results'})
    laptops = container.ul.find_all('div', class_='s-item__info')
    print(len(laptops))
    for laptop in laptops:
        if laptop.find('span', attrs={'role': 'heading'}) is not None:
            name = laptop.find('span', attrs={'role': 'heading'}).text
        else:
            name = 'Bilgi yok'
        laptop_dict['name'].append(name)

        if laptop.find('span', class_='s-item__price') is not None:
            price = laptop.find('span', class_='s-item__price').text
        else:
            price = 'Bilgi yok'
        laptop_dict['price'].append(price)

        if laptop.find('span', class_='s-item__logisticsCost') is not None:
            shipping = laptop.find('span', class_='s-item__logisticsCost').text
        else:
            shipping = 'Bilgi yok'
        laptop_dict['shipping'].append(shipping)

        if laptop.find('a', class_='s-item__link') is not None:
            link = laptop.find('a', class_='s-item__link')['href']
        else:
            link = 'Bilgi yok'
        laptop_dict['link'].append(link)

    next_as_button = soup.find('button', class_='pagination__next')
    if next_as_button is not None:
        break

    page_no += 1

df = pd.DataFrame(laptop_dict)
df.to_excel('laptops.xlsx')

