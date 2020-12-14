import requests
from bs4 import BeautifulSoup
import csv
import time

headers = {
    'user-agent': '',
    'accept': ''}
file = 'jobs.csv'
url = input('Введите желаемую страницу из авито/вакансии: ')
url1 = url[0:-2]


def get_html(url, params):
    time.sleep(1)
    r = requests.get(url, headers=headers, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='pagination-item-1WyVp')
    count = int(pagination[3].get_text())
    return count


def save_file(items, path):
    with open(path, 'w', newline='') as fl:
        writer = csv.writer(fl, delimiter=';')
        writer.writerow(['Профессия', 'Ссылка', 'Зарплата', 'Город', 'Дата публикации'])
        for item in items:
            writer.writerow([item['job title'], item['link'], item['salary'], item['city'],
                             item['post_time'].encode('utf-8').decode('utf-8')])


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='iva-item-body-NPl6W')
    jobs = []
    for item in items:
        jobs.append({'job title': item.find('div', 'iva-item-titleStep-2bjuh').get_text(strip=True),
                     'link': 'https://www.avito.ru/' + item.find('div', 'iva-item-titleStep-2bjuh').find_next('a').get(
                         'href'),
                     'salary': item.find('span', 'price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo').get_text(
                         strip=True),
                     'city': item.find('span', 'geo-address-9QndR text-text-1PdBw text-size-s-1PUdo').get_text(
                         strip=True),
                     'post_time': item.find('div', 'date-root-3w7Ry').get_text(strip=True)})
    return jobs


def find_this(lists, job_title='', min_salary='', city='', save='yes', possible_post_time=''):
    def add(item, filter):
        if item not in filter:
            filter.append(item)

    filtered_items = []
    for item in lists:
        try:
            if job_title in item['job title']:
                add(item, filtered_items)
            if int(min_salary) < int(item['salary'].replace('₽', '').replace(' ', '')):
                add(item, filtered_items)
            if city in item['city']:
                add(item, filtered_items)
            if item['post_time'] in possible_post_time:
                add(item, filtered_items)
            else:
                pass
        except:
            pass
    print(filtered_items)
    if save.lower() == 'yes':
        fl = 'filtered_jobs.csv'
        save_file(filtered_items, fl)


def parse():
    html = get_html(url, params=None)
    if html.status_code == 200:
        jobs2 = []
        count = get_pages_count(html.text)
        for page in range(1, count + 1):
            time.sleep(1)
            print(f'Парсинг странциы:{page} из {count}')
            html1 = get_html(url1 + '=' + str(page), params=None)
            print(url1 + '=' + str(page))
            jobs2.extend(get_content(html1.text))
        print('Получено {} вакансий'.format(len(jobs2)))
        save_file(jobs2, file)
        print(jobs2)
        find_this(jobs2, 'Администратор')
    else:
        print(html.status_code)


parse()


