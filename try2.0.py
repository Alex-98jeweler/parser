import requests
from bs4 import BeautifulSoup
import time
import csv
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
}
FILE = 'tatarstan.csv'





r = requests.get(f'https://tat-job.ru/tatarstan/vakansii/page19.html', headers = HEADERS)

soup = BeautifulSoup(r.text, 'html.parser')

a = soup.find_all('td', class_='info-item')
links = []
for i in a:
    b = i.find('a')
    if b == None:
        continue
    else:
        b = i.find('a').get('href')
    links.append(b)

vacancies = []
for link in links:
    r = requests.get(f'https://tat-job.ru{link}', headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    a = soup.find('body')
    category = a.find('ul', class_='breadcrumb').find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().getText()
    name = a.find('h1').get_text()
    salary = a.find_all('strong')
    salary = salary[1].get_text()
    table = a.find('table', class_='table table-striped')
    table = table.find_all('div')
    if len(table) < 4:
        continue
    zanyat = table[0].get_text()
    schedule = table[1].get_text()
    exp = table[2].get_text()
    education = table[3].get_text()
    date_of_public = a.find('div', class_='info-add-ads pull-left').find_next().find_next().find_next().find_next().get_text()
    description = a.find('p').get_text()
    name_company = a.find('h3').get_text()
    address = a.find('strong', itemprop='address').get_text(strip=True)
    vacancies.append({
        'category': category,
        'name': name,
        'salary': salary,
        'employment': zanyat,
        'schedule': schedule,
        'experience': exp,
        'education': education,
        'name company': name_company,
        'address': address,
        'date of public': date_of_public.replace('Сегодня', '02.11.2010').replace('Вчера', '01.11.2020').replace('в', ''),
        'description': description
    })

with open(FILE, 'a', newline='', errors='ignore') as file:
    writer = csv.writer(file, delimiter=';')
    #writer.writerow(['Раздел', 'Название', 'Зарплата', 'Занятость', 'График','Опыт', 'Образование', 'Название компании', 'Адрес','Дата Публикации', 'Детальное описание' ])
    for item in vacancies:
        writer.writerow([item['category'], item['name'], item['salary'], item['employment'], item['schedule'],
                         item['experience'], item['education'], item['name company'], item['address'], item['date of public'],
                         item['description']])


