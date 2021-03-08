from bs4 import BeautifulSoup
import requests
import csv

URL_CATEGORIES = ["/rabota/vbranch25/","/rabota/vbranch17/","/rabota/vbranch18/","/rabota/vbranch6/","/rabota/vbranch13/","/rabota/vbranch5/","/rabota/vbranch4/","/rabota/vbranch37/","/rabota/vbranch104/","/rabota/vbranch7/","/rabota/vbranch36/","/rabota/vbranch16/","/rabota/vbranch38/","/rabota/vbranch39/","/rabota/vbranch22/","/rabota/vbranch40/","/rabota/vbranch41/","/rabota/vbranch23/","/rabota/vbranch14/","/rabota/vbranch42/","/rabota/vbranch26/"]
HOST = 'https://66.ru'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
}
FILE = '66_ru.csv'

for url in URL_CATEGORIES:
    for page in range(1,5):
        c = []
        r = requests.get(f'https://66.ru{url}?page={page}', headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        a = soup.find_all('td', class_='vacancyShort__description')
        if len(a) == 0:
            break
        for i in a:
            c.append(
                i.find('a', class_='vacancyShort__title').get('href')
            )


        vacansies = []
        for i in c:
            r = requests.get(HOST + i.strip(), headers=HEADERS)
            soup = BeautifulSoup(r.text, 'html.parser')
            vacancy = soup.find('div', class_='ie_layout')
            var = vacancy.find('div', class_='onejob-right-top')
            salary = vacancy.find('td', class_='left')
            schedule = vacancy.find('tr', class_='odd')
            experience = vacancy.find('tr', class_='odd')
            education = vacancy.find('tr', class_='odd')
            name_company = vacancy.find('div', class_='contact')
            contacts = vacancy.find('h4')
            date = vacancy.find('span', class_='time-add-value')
            city = vacancy.find('div', class_='onejob-right-top')
            if date == None:
                date = "Не могу извлечь"
            else:
                date = date.getText()
            if contacts == None:
                contacts = 'Не могу извлечь'
            else:
                contacts = contacts.find_next().find_next().get_text(strip=True)
            if name_company == None:
                name_company = 'Не могу найти'
            else:
                name_company = name_company.find('h3', class_='company').get_text()
            if education == None:
                education = 'Не могу найти'.replace('\n', '').replace('\t', '')
            else:
                education = education.find_next().find_next().find_next().find_next().find_next().find_next().find('td',
                                                                                                                   class_='right').get_text(
                    strip=True)
            if experience == None:
                experience = 'Не могу найти'
            else:
                experience = experience.find_next().find_next().find_next().find('td', class_='right').get_text(
                    strip=True)
            if schedule == None:
                schedule = 'Нету'
            else:
                schedule = schedule.find('td', class_='right').get_text()
            if salary == None:
                salary = 'Не указано'
            else:
                salary = salary.find_next().getText(strip=True).replace('\xa0', '')
            if var == None:
                var = 'Возникла ошибка извлечения'.replace('\n', '').replace('\t', '')

            else:
                var = var.find('p').getText(strip=True).replace('\u200b', '').replace('\xa0', '').replace('Распечатать', '').replace('\u200e', '')
            if city == None:
                city = "Not found"
            else:
                city = city.find('h3').get_text()
            city1 = ''
            for sign in city:
                city1 += sign
                if sign == ',':
                    break
            vacansies.append({
                'category': vacancy.find('div', class_='content-block').find_next().find_next().get_text().replace('\n',
                                                                                                                   '').replace(
                    '\t', '').replace('\u200e', '').replace('\u20bd', '').replace('\u2219', '').replace('\xfc', '').replace('\u0450', ''),
                'name': vacancy.find('h1').get_text().replace('\u200e', '').replace('\u20bd', '').replace('\u2219', '').replace('\xfc', '').replace('\u0450', '').replace('\u2062', ''),
                'salary': salary.replace('\u200e', '').replace('\u20bd', '').replace('\u2219', '').replace('\xfc', '').replace('\u0450', ''),
                'schedule': schedule.replace('\u200e', '').replace('\u20bd', '').replace('\u2219', '').replace('\xfc', '').replace('\u0450', ''),
                'experience': experience.replace('\u200e', '').replace('\u20bd', '').replace('\u2219', '').replace('\xfc', '').replace('\u0450', ''),
                'education': education.replace('\u200e', '').replace('\u20bd', '').replace('\u2219', '').replace('\xfc', '').replace('\u0450', ''),
                'company': name_company.replace('\u200e', '').replace('\u20bd', '').replace('\u2219', '').replace('\xfc', '').replace('\u0450', ''),
                'city': city1,
                'contact': contacts.replace('\u200e', '').replace('\u20bd', '').replace('\u2219', '').replace('\xfc', '').replace('\u0450', ''),
                'date_of_publication': date.replace('\u200e', '').replace('\u20bd', '').replace('\u2219', '').replace('\xfc', '').replace('\u0450', ''),
                'description': var.replace('\u200e', '').replace('\u20bd', '').replace('\u2219', '').replace('\xfc', '').replace('\u0450', '').replace('\n', '')

            })

        with open(FILE, 'a', newline='', errors='ignore') as file:
            writer = csv.writer(file, delimiter=';')
            #writer.writerow(['Раздел', 'Название', 'Зарплата', 'График', 'Опыт', 'Образование','Название компании', 'Город', 'Контактная информация', 'Дата Публикации', 'Детальное описание'])
            for item in vacansies:
                writer.writerow([item['category'], item['name'], item['salary'], item['schedule'], item['experience'],
                                 item['education'], item['company'],item['city'], item['contact'], item['date_of_publication'],
                                 item['description']])