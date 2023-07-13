import requests
import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from fake_useragent import UserAgent

ua = UserAgent()
ua_ = ua.random

date_start = '30.12.2022'
date_stop = '3.01.2023'

start = datetime.strptime(date_start, '%d.%m.%Y').date()
stop = datetime.strptime(date_stop, '%d.%m.%Y').date()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": f'{ua}'
}

cookies = {
    'pll_language': 'uk',
    '_gid': 'GA1.2.1810776591.1689236007',
    'TS01a65230': '01217fbce07a931ba059c076242ed957f0b719c0bdd95f7bc8555e73a9b527879cbfbf22e053a0de913cf0a20899e44d99709e8ac0',
    'TSca37abee027': '08124a4360ab2000cd41a7453b871bbfb1717fa0c8155bf6c11934aa88f4a0bf48dffd1181d1eea00884e23b0b113000495a16896685023923956420bc794a9fff40e74f807386da9950f2b4449a59449a99e781868d5607d2e39c8132bafc19',
    '__cf_bm': '_dquT0kH4_ks50srEnbFPbRCUe3v6biwltfQ3V3o_Ho-1689237030-0-Ae28YhD80+KqpkNj7W+rknjLkQhEX4r+shnY/axAJlTxaFNPIwl7V4EyPrpC8Cko/4aXN7P3KKx0oFe3eNw8HYM=',
    '_ga_C1EFLWK2ZZ': 'GS1.1.1689236006.2.1.1689237031.0.0.0',
    '_ga': 'GA1.1.2093891621.1687346240',
}

print('start...')

url = 'https://ua.energy/uchasnikam_rinku/auktsiony/rezultaty-auktsioniv-z-dostupu-do-mizhderzhavnyh-peretyniv/'

response = requests.get(url=url, cookies=cookies, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
cq_tabcontent = soup.find_all('div', class_='cq-tabcontent style2')

arr_ = []

date_pattern = r'\d{2}\.\d{2}\.\d{4}'

for item in cq_tabcontent:
    aaa = item.find_all('a')
    for url__ in aaa:
        url_ = url__.get('href')

        pattern = r'https?://[^\s]+\.xlsx'

        if re.findall(pattern, url_):
            arr_.append(url_)

            match = re.search(date_pattern, url_)
            if match:
                date = match.group(0)
                date = date.replace('-', '')

                date_object = datetime.strptime(date, "%d.%m.%Y")
                formatted_date = date_object.strftime("%Y%m%d")
                file_name = f'{formatted_date}.xls'

                file_date = datetime.strptime(formatted_date, "%Y%m%d").date()

                if start <= file_date <= stop:
                    response = requests.get(url_, headers=headers)

                    filename = f'{formatted_date}.xlsx'

                    with open(filename, "wb") as file:
                        file.write(response.content)

                    print(f"File: {filename} >>> downloaded successfully.")
