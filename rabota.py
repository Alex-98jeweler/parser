from bs4 import BeautifulSoup
import requests
import csv

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
}
URL_CATEGORIES = ["/rabota/vbranch106/", "/rabota/vbranch25/", "/rabota/vbranch17/","/rabota/vbranch18/","/rabota/vbranch6/","/rabota/vbranch13/","/rabota/vbranch5/","/rabota/vbranch4/","/rabota/vbranch37/","/rabota/vbranch104/","/rabota/vbranch7/","/rabota/vbranch36/","/rabota/vbranch16/","/rabota/vbranch38/","/rabota/vbranch39/","/rabota/vbranch22/","/rabota/vbranch40/","/rabota/vbranch41/","/rabota/vbranch23/","/rabota/vbranch14/","/rabota/vbranch42/","/rabota/vbranch26/"]
HOST = 'https://66.ru'
URL = 'https://66.ru/rabota/vbranch106/'
result = []
FILE = '66_ru.csv'
c = []
d = []

for num in range(2, 5):
    r = requests.get(f'https://66.ru/rabota/vbranch106/?page={num}', headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    a = soup.find_all('td', class_='vacancyShort__description')
    for i in a:
        c.append(
                i.find('a', class_='vacancyShort__title').get('href')
        )


    print(c)



    vacansies = []
    for i in c:
        r = requests.get(HOST + i.strip(), headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        vacancy = soup.find('div', class_='ie_layout')
        var = vacancy.find('div', class_='onejob-right-top')
        salary = vacancy.find('td', class_='left')
        schedule = vacancy.find('tr', class_='odd')
        experience = vacancy.find('tr', class_='odd')
        education = vacancy.find('tr',class_='odd')
        name_company =  vacancy.find('div', class_='contact')
        contacts = vacancy.find('h4')
        date = vacancy.find('span', class_='time-add-value')
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
            education = education.find_next().find_next().find_next().find_next().find_next().find_next().find('td', class_='right').get_text(strip=True)
        if experience == None:
            experience = 'Не могу найти'
        else:
            experience = experience.find_next().find_next().find_next().find('td',class_='right').get_text(strip=True)
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
            var = var.getText(strip=True).replace('\u200b', '').replace('\xa0', '').replace('Распечатать', '')

        vacansies.append({
            'category': vacancy.find('div', class_='content-block').find_next().find_next().get_text().replace('\n', '').replace('\t', ''),
            'name': vacancy.find('h1').get_text(),
            'salary': salary,
            'schedule': schedule,
            'experience': experience,
            'education': education,
            'company': name_company,
            'contact': contacts,
            'date_of_publication': date,
            'description': var


        })
    print(vacansies)

    with open(FILE, 'a', newline='', errors='ignore') as file:
        writer = csv.writer(file, delimiter=';')
        #writer.writerow(['Раздел', 'Название', 'Зарплата', 'График', 'Опыт', 'Образование','Название компании', 'Контактная информация', 'Дата Публикации', 'Детальное описание'])
        for item in vacansies:
            writer.writerow([item['category'], item['name'], item['salary'], item['schedule'],item['experience'],item['education'],item['company'],item['contact'],item['date_of_publication'], item['description']])



