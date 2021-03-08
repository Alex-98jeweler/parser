import requests
from bs4 import BeautifulSoup
import csv
import os


HOST = 'https://quke.ru'
URL = 'https://quke.ru/shop/smartfony'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
}
FILE = "rabota66.csv"


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='pagination2__page')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='b-card2__inner')
    phones = []

    for item in items:
        phones.append({
            'title': item.find('a', class_='b-card2__name').get_text(strip=True),
            'price': item.find('span', class_='b-card2__price-val').get_text(),
            'availability': item.find('div', class_='b-card2__status-text').get_text(),
            'link': HOST + item.find('a', class_='b-card2__name').get('href')
        })
    return phones

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Модель', 'Цена', 'В наличии или предзаказ', 'Ссылка',])
        for item in items:
            writer.writerow([item['title'], item['price'], item['availability'], item['link']])

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        phones = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Идет парсинг страницы{page} из {pages_count}...')
            html = get_html(URL, params={'page':page})
            phones.extend(get_content(html.text))
        save_file(phones, FILE)
        print(f'Получено {len(phones)} смартфонов')
        os.startfile(FILE)
    else:
        print("Error")

parse()






