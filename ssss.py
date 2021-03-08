from bs4 import BeautifulSoup
import requests


HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
}
r = requests.get('https://krasnodar.kupiprodai.ru/rabota/krasnodar_vakansii_informacionnyy_konsultant_pk_5429586', headers=HEADERS)


soup = BeautifulSoup(r.text, 'html.parser')

a = soup.find('h1')

print(a)






