import requests
import json
import time

import sys

import csv

import calendar
from datetime import datetime, timedelta

date_start = '1.03.2022'
date_stop = '30.06.2023'

# Преобразуем строки с датами в объекты datetime
start = datetime.strptime(date_start, '%d.%m.%Y')
stop = datetime.strptime(date_stop, '%d.%m.%Y')

cookies = {
    '_gid': 'GA1.3.785657314.1687156607',
    'lang': 'ukr',
    'PHPSESSID': '2n2adt8bm187iajjdsbu0ndsg1',
    '_ga_SX032CTY0J': 'GS1.1.1687328127.7.1.1687328788.0.0.0',
    '_ga': 'GA1.3.484492776.1687156607',
    '_gat_gtag_UA_144367606_1': '1',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,vi;q=0.5,pt;q=0.4,ka;q=0.3',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '_gid=GA1.3.785657314.1687156607; lang=ukr; PHPSESSID=2n2adt8bm187iajjdsbu0ndsg1; _ga_SX032CTY0J=GS1.1.1687328127.7.1.1687328788.0.0.0; _ga=GA1.3.484492776.1687156607; _gat_gtag_UA_144367606_1=1',
    'Origin': 'https://www.oree.com.ua',
    'Referer': 'https://www.oree.com.ua/index.php/IDM_graphs',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def pro(a_, b_):
    c_ = (b_ / a_) * 100 - 100
    return f'{c_:.2f}'


arr_hours_ = []

# Перебираем все месяца в заданном диапазоне
current_month = start

while current_month <= stop:
    year__ = current_month.strftime('%Y')
    month__ = current_month.strftime('%m')
    days_in_month = calendar.monthrange(int(year__), int(month__))[1]

    for dd_ in range(1, days_in_month + 1):

        ttt_ = current_month.strftime('%Y-%m')
        ttt = f'{ttt_}-{dd_:02d}'
        # print(f'ttt --- >>> {ttt}')

        # Формируем ключ для текущего месяца (год и месяц в формате YYYY-MM)
        key = current_month.strftime('%m.%Y')
        key_ = current_month.strftime('%m.%Y')

        key__ = f'{dd_:02d}.{key}'

        print(key__)
        time.sleep(0.3)

        data = {
            'date': f'{key__}',  # 18.06.2023
            'shopping_area': 'OES',
            'market': 'DAM',
        }

        try:
            response = requests.post(
                'https://www.oree.com.ua/index.php/IDM_graphs/get_data_for_chart_DSAP',
                cookies=cookies,
                headers=headers,
                data=data,
            )

            data_ = json.loads(response.text)

            for i in range(0, 24):

                ts = f"{i:02d}:00:00"
                hour_ = f'{ttt} {ts}'

                declared_sell_ = data_["sell"][i + 24]
                declared_buy_ = data_["buy"][i + 24]
                changing_sell_ = pro(float(data_["sell"][i]), float(declared_sell_))
                changing_buy_ = pro(float(data_["buy"][i]), float(declared_buy_))
                deficit_surplus_ = float(declared_sell_) - float(declared_buy_)

                # print(f'{declared_sell_} --->>> {declared_buy_} --->>> {changing_sell_} --->>> {changing_buy_} --->>> {deficit_surplus_:.2f}')

                arr_hours_.append(
                    {
                        "Hour": hour_,
                        "Declared_SELL": declared_sell_,
                        "Declared_BUY": declared_buy_,
                        "Changing_SELL": changing_sell_,
                        "Changing_BUY": changing_buy_,
                        "Deficit_Surplus": f'{deficit_surplus_:.2f}'
                    }
                )

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Тип исключения:", exc_type)
            print("Сообщение об ошибке:", exc_value)
            break

    # Переходим к следующему месяцу
    current_month = current_month + timedelta(days=32)
    current_month = current_month.replace(day=1)


with open(f'___!!!_2.json', 'w+', encoding='utf-8') as file:
    json.dump(arr_hours_, file, indent=4, ensure_ascii=False)

with open('___!!!_2.csv', "w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=arr_hours_[0].keys())
    writer.writeheader()
    writer.writerows(arr_hours_)
