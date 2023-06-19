import requests
import json
import time

from bs4 import BeautifulSoup

import re
# import pandas as pd

import csv
# Чтение данных из файла
with open('___!!!.json', 'r') as file:
    data = json.load(file)

# Открываем CSV-файл для записи
with open('___!!!.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')

    # Записываем заголовки столбцов
    writer.writerow(['Year-Month', 'Date', 'Values'])

    # Записываем данные
    for year_month, dates in data.items():
        for date, values in dates.items():
            for value in values:
                writer.writerow([year_month, date, value])
breakpoint()


from datetime import datetime, timedelta

date_start = '01.03.2022'
date_stop = '31.05.2023'

# Преобразуем строки с датами в объекты datetime
start = datetime.strptime(date_start, '%d.%m.%Y')
stop = datetime.strptime(date_stop, '%d.%m.%Y')

# Создаем словарь, где ключами будут год и месяц, а значениями - события
events_by_month = {}

cookies = {
    '_gid': 'GA1.3.785657314.1687156607',
    'PHPSESSID': '5d78539gum179dkmhhq8vqgv07',
    '_gat_gtag_UA_144367606_1': '1',
    '_ga_SX032CTY0J': 'GS1.1.1687158699.2.1.1687158769.0.0.0',
    '_ga': 'GA1.1.484492776.1687156607',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,vi;q=0.5,pt;q=0.4,ka;q=0.3',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '_gid=GA1.3.785657314.1687156607; PHPSESSID=5d78539gum179dkmhhq8vqgv07; _gat_gtag_UA_144367606_1=1; _ga_SX032CTY0J=GS1.1.1687158699.2.1.1687158769.0.0.0; _ga=GA1.1.484492776.1687156607',
    'Origin': 'https://www.oree.com.ua',
    'Referer': 'https://www.oree.com.ua/index.php/pricectr',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


data__ = {}

# Перебираем все месяца в заданном диапазоне
current_month = start
while current_month <= stop:
    # Формируем ключ для текущего месяца (год и месяц в формате YYYY-MM)
    key = current_month.strftime('%Y-%m')
    key_ = current_month.strftime('%m.%Y')

    month_year = key
    data__[month_year] = {}
    day_data = data__[month_year]

    print(key_)
    time.sleep(1)

    # Если ключа еще нет в словаре, добавляем его с пустым списком событий
    if key not in events_by_month:
        events_by_month[key] = []

    data = {
        'date': f'{key_}',
        'market': 'DAM',
        'zone': 'IPS',
    }

    response = requests.post('https://www.oree.com.ua/index.php/pricectr/data_view', cookies=cookies, headers=headers,
                             data=data)

    soup = BeautifulSoup(response.text, 'lxml')
    tr_ = soup.find('tbody').find_all('tr')

    # tmp_ = '03_mart'
    arr_ = []

    for r__ in tr_:
        td_ = r__.find_all('td')

        arr_items = []

        for i, d__ in enumerate(td_):
            if i == 0:
                # string = '<td>\n 01.06.2023 &lt;\/td&gt;\n </td>'

                # Находим все последовательности цифр и точек, расположенные между пробелами или символами переноса строки
                matches = re.findall(r'[\d\.]+', str(d__))

                # Если найдено несколько совпадений, берем первое
                if len(matches) > 0:
                    date_ = matches[0]
                    day_data[date_] = []


            else:
                matches = re.findall(r'[\d\.]+', str(d__))

                if len(matches) > 0:
                    item = matches[0]
                    day_data[date_].append(item)


    # Добавляем события в список для текущего месяца (здесь может быть ваш код для анализа событий)
    # events_by_month[key].append('Some event')

    # Переходим к следующему месяцу
    current_month = current_month + timedelta(days=32)
    current_month = current_month.replace(day=1)


# Выводим результаты анализа
# for month, events in events_by_month.items():
#     print(month)
#     print(events)
#     print('---')



with open(f'___!!!.json', 'w+', encoding='utf-8') as file:
    json.dump(data__, file, indent=4, ensure_ascii=False)

# df = pd.read_json(r'___!!!.json')
# df.to_csv(r'___!!!.csv', index=None)

# # Создание CSV-файла
# with open("___!!!.csv", "w", newline='') as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerow(["Month and Year", "Date", "Value"])
#
#     for month_year, day_data in data.items():
#         for date, values in day_data.items():
#             for value in values:
#                 writer.writerow([month_year, date, value])

# # Создание CSV-файла
# with open("data.csv", "w", newline='') as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerow(["Month and Year", "Date", "Value"])
#
#     for month_year, day_data in data.items():
#         for date, values in day_data.items():
#             for value in values:
#                 writer.writerow([month_year, date, value])

# # Создание CSV-файла
# with open("data.csv", "w", newline='') as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerow(["Месяц и год", "Дата", "Значение"])
#
#     for month_year, day_data in data.items():
#         for date, values in day_data.items():
#             for value in values:
#                 writer.writerow([month_year, date, value])
