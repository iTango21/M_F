import requests
import json
import time

from bs4 import BeautifulSoup
import lxml

import re
import pandas as pd


# url = 'https://www.flipkart.com/'


df = pd.read_json(r'___!!!_1.json')
df.to_csv(r'___!!!_1.csv', index=None)

breakpoint()

import csv

import calendar
from datetime import datetime, timedelta

date_start = '1.03.2022'
date_stop = '30.06.2023'

# Преобразуем строки с датами в объекты datetime
start = datetime.strptime(date_start, '%d.%m.%Y')
stop = datetime.strptime(date_stop, '%d.%m.%Y')

# Создаем словарь, где ключами будут год и месяц, а значениями - события
events_by_month = {}

cookies = {
    '_gid': 'GA1.3.785657314.1687156607',
    'PHPSESSID': 'gd2q488racdr5u8v0lv8h2tir7',
    '__e_inc': '1',
    'lang': 'ukr',
    '_gat_gtag_UA_144367606_1': '1',
    '_ga_SX032CTY0J': 'GS1.1.1687179861.4.1.1687182987.0.0.0',
    '_ga': 'GA1.3.484492776.1687156607',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,vi;q=0.5,pt;q=0.4,ka;q=0.3',
    'Connection': 'keep-alive',
    # 'Content-Length': '0',
    # 'Cookie': '_gid=GA1.3.785657314.1687156607; PHPSESSID=gd2q488racdr5u8v0lv8h2tir7; __e_inc=1; lang=ukr; _gat_gtag_UA_144367606_1=1; _ga_SX032CTY0J=GS1.1.1687179861.4.1.1687182987.0.0.0; _ga=GA1.3.484492776.1687156607',
    'Origin': 'https://www.oree.com.ua',
    'Referer': 'https://www.oree.com.ua/index.php/control/results_mo/DAM',
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
day__ = {}

# Перебираем все месяца в заданном диапазоне
current_month = start
while current_month <= stop:
    year__ = current_month.strftime('%Y')
    month__ = current_month.strftime('%m')
    days_in_month = calendar.monthrange(int(year__), int(month__))[1]

    arr_month_ = []

    for dd_ in range(1, days_in_month + 1):
        # print(f'Day = {dd_}')

        arr_hours_ = []

        ttt_ = current_month.strftime('%Y-%m')
        ttt = f'{ttt_}-{dd_:02d}'
        # print(f'ttt --- >>> {ttt}')

        # Формируем ключ для текущего месяца (год и месяц в формате YYYY-MM)
        key = current_month.strftime('%m.%Y')
        key_ = current_month.strftime('%m.%Y')

        key__ = f'{dd_:02d}.{key}'

        # year_month = key__

        year_month = ttt_

        # print(key)
        print(key__)
        time.sleep(0.3)

        try:
            response = requests.post(
                f'https://www.oree.com.ua/index.php/PXS/get_pxs_hdata/{key__}/DAM/2',
                cookies=cookies,
                headers=headers,
            )

            data_ = json.loads(response.text)

            # print(data_)
            # print(data_['html'])


            soup = BeautifulSoup(data_['html'], 'lxml')
            tr_ = soup.find('tbody').find_all('tr')

            arr_ = []
            records = {}

            for r__ in tr_:
                td_ = r__.find_all('td')

                # https://www.oree.com.ua/index.php/control/results_mo/DAM

                Hour_ = td_[1].text.strip()  # Hour

                # ts = f"{ttt} {int(Hour_) - 1:02d}:00:00"
                ts = f"{int(Hour_) - 1:02d}:00:00"

                Price_ = td_[2].text.strip()                        # Price, uah/MWh
                Sales_volume_ = td_[3].text.strip()                 # Sales volume, MW.h
                Purchase_volume_ = td_[4].text.strip()              # Purchase volume, MW.h
                Declared_sales_volume_ = td_[5].text.strip()        # Declared sales volume, MW.h
                Declared_purchase_volume_ = td_[6].text.strip()     # Declared purchase volume, MW.h

                arr_hours_.append(
                    {
                        "Hour": ts,
                        "Price": Price_,
                        "Sales volume": Sales_volume_,
                        "Purchase volume": Purchase_volume_,
                        "Declared sales volume": Declared_sales_volume_,
                        "Declared purchase volume": Declared_purchase_volume_
                    }
                )
        except:
            break

        day__[ttt] = arr_hours_

    data__[year_month] = day__


    # Переходим к следующему месяцу
    current_month = current_month + timedelta(days=32)
    current_month = current_month.replace(day=1)



with open(f'___!!!_1.json', 'w+', encoding='utf-8') as file:
    json.dump(data__, file, indent=4, ensure_ascii=False)

# # Создание CSV-файла
# with open("___!!!_1.csv", "w", newline="", encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Year-Month", "Date-Time", "Values"])
#
#     for month, records in data__.items():
#         for timestamp, value in records.items():
#             writer.writerow([month, timestamp, value])
