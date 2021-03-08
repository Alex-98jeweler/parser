from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
import os


FILE = 'tatarstan1.csv'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
}

# r = requests.get('http://opendata.trudvsem.ru/api/v1/vacancies?offset=1&limit=100&createdFrom=2020-10-21T00:00:00Z').json()
vacacy = []
vacancies = []
#
# data = r['results']['vacancies'][22]['vacancy']
# print((data))

for item in range(1,150):
    r = requests.get(f'http://opendata.trudvsem.ru/api/v1/vacancies/region/16?offset={item}&limit=100').json()
    vacacy = []
    if 'results' in r:
        for i in range(len(r['results']['vacancies'])):
            if 'duty' in r['results']['vacancies'][i]['vacancy']:
                descript = r['results']['vacancies'][i]['vacancy']['duty'].replace('<p>', '').replace('</p>', '')
            else:
                descript = 'Нет'
            if 'qualification' in r['results']['vacancies'][i]['vacancy']['requirement']:
                descript1 = r['results']['vacancies'][i]['vacancy']['requirement']['qualification'].replace('<p>', '').replace('</p>', '')
            else:
                descript1 = ''
            if 'education' in r['results']['vacancies'][i]['vacancy']['requirement']:
                a = r['results']['vacancies'][i]['vacancy']['requirement']['education']
            else:
                a = 'не указано'
            if 'phone' in r['results']['vacancies'][i]['vacancy']['company']:
                phone = r['results']['vacancies'][i]['vacancy']['company']['phone']
            else:
                phone = 'Не указан'
            if 'email' in r['results']['vacancies'][i]['vacancy']['company']:
                email = r['results']['vacancies'][i]['vacancy']['company']['email']
            else:
                email = "Не указан"
            if 'schedule' in r['results']['vacancies'][i]['vacancy']:
                schedule = r['results']['vacancies'][i]['vacancy']['schedule']
            else: schedule = "Не указано"
            vacancies.append({
                'category': r['results']['vacancies'][i]['vacancy']['category']['specialisation'] ,
                'name': r['results']['vacancies'][i]['vacancy']['job-name'],
                'salary': r['results']['vacancies'][i]['vacancy']['salary'],
                'schedule': schedule,
                'employment': r['results']['vacancies'][i]['vacancy']['employment'],
                 'educations': a ,
                 'experience': r['results']['vacancies'][i]['vacancy']['requirement']['experience'],
                'city': r['results']['vacancies'][i]['vacancy']['addresses']['address'][0]['location'],
                'region':r['results']['vacancies'][i]['vacancy']['region']['name'],
                'name_company': r['results']['vacancies'][i]['vacancy']['company']['name'],
                'phone': phone,
                'e-mail': email,
                'created_date': r['results']['vacancies'][i]['vacancy']['creation-date'],
                 'modify_date': r['results']['vacancies'][i]['vacancy']['modify-date'],
                'description': (descript + descript1).replace('<br/>', " ")


            })


    else:
        break

for j in range(len(vacancies)):
    for k in vacancies[j + 1:]:
        if vacancies[j] == k:
            vacancies.remove(vacancies[j])

with open(FILE, 'w', newline='', errors='ignore') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Раздел', 'Название вакансии', 'Зарплата', 'График работы', 'Занятость', 'Образование', 'Опыт Работы', 'Город', 'Регион', 'Название Компании','Телефон','E-Mail' ,'Дата публикации', 'Дата модерации', 'Описание'])
    for item in vacancies:
        writer.writerow([item['category'], item['name'], item['salary'], item['schedule'], item['employment'],item['educations'], item['experience'], item['city'], item['region'], item['name_company'],item['phone'], item['e-mail'], item['created_date'], item["modify_date"], item['description']])

