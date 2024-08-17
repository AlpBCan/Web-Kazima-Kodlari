import requests
import os

os.mkdir('book_images')

with open('image_links.txt', 'r') as f:
    links_text = f.read()
    links_list = links_text.split('\n')
    print(len(links_list))

for i, image_url in enumerate(links_list):
    response = requests.get(image_url)
    with open(f'book_images/{i+1}.jpg', 'wb') as imagefile:
        imagefile.write(response.content)