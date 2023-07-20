import os
import re
import datetime
from datetime import datetime as dt, timedelta


import pandas as pd
import csv
import openpyxl
from transliterate import translit

import requests
from bs4 import BeautifulSoup

from fake_useragent import UserAgent

ua = UserAgent()
ua_ = ua.random

# Replace with your path!
folder_path = 'D:\\_work_2023_\\programming\\Python\\0 _ freelance _ 0\\upw\\M_F\\'
# folder_path = 'D:\\_work_\\programming\\Python\\0 _ freelance _ 0\\upw\\M_F\\'

output_file = 'join_csv.csv'

date_start = '1.4.2022'
date_stop = '1.7.2023'

start = dt.strptime(date_start, '%d.%m.%Y').date()
stop = dt.strptime(date_stop, '%d.%m.%Y').date()


def get_ua_data(start_time, end_time, folder_path):

    # headers = {
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #     "User-Agent": f'{ua}'
    # }
    #
    # cookies = {
    #     'pll_language': 'uk',
    #     '_gid': 'GA1.2.1810776591.1689236007',
    #     'TS01a65230': '01217fbce07a931ba059c076242ed957f0b719c0bdd95f7bc8555e73a9b527879cbfbf22e053a0de913cf0a20899e44d99709e8ac0',
    #     'TSca37abee027': '08124a4360ab2000cd41a7453b871bbfb1717fa0c8155bf6c11934aa88f4a0bf48dffd1181d1eea00884e23b0b113000495a16896685023923956420bc794a9fff40e74f807386da9950f2b4449a59449a99e781868d5607d2e39c8132bafc19',
    #     '__cf_bm': '_dquT0kH4_ks50srEnbFPbRCUe3v6biwltfQ3V3o_Ho-1689237030-0-Ae28YhD80+KqpkNj7W+rknjLkQhEX4r+shnY/axAJlTxaFNPIwl7V4EyPrpC8Cko/4aXN7P3KKx0oFe3eNw8HYM=',
    #     '_ga_C1EFLWK2ZZ': 'GS1.1.1689236006.2.1.1689237031.0.0.0',
    #     '_ga': 'GA1.1.2093891621.1687346240',
    # }
    #
    # print('start...')
    #
    # url = 'https://ua.energy/uchasnikam_rinku/auktsiony/rezultaty-auktsioniv-z-dostupu-do-mizhderzhavnyh-peretyniv/'
    #
    # response = requests.get(url=url, cookies=cookies, headers=headers)
    # soup = BeautifulSoup(response.text, 'lxml')
    # cq_tabcontent = soup.find_all('div', class_='cq-tabcontent style2')
    #
    # arr_ = []
    # formatted_date = ''
    #
    # # date_pattern = r'\d{2}\.\d{2}\.\d{4}'
    # # date_pattern = r'\d{2}[-.]\d{2}[-.]\d{4}'  # Updated date pattern to handle various date formats
    # # date_patterns = [
    # #     r'\d{2}\.\d{2}\.\d{4}',  # Format: 01.07.2023
    # #     r'\d{2}[-.]\d{2}[-.]\d{4}',  # Format: 01-07-2023 or 01.07-2023
    # #     r'\d{2}_\d{2}_\d{4}'  # Format: 29_10_2022
    # # ]
    # date_patterns = [
    #     r'\d{2}\.\d{2}\.\d{4}',  # Format: 01.07.2023
    #     r'\d{2}[-.]\d{2}[-.]\d{4}',  # Format: 01-07-2023 or 01.07-2023
    #     r'\d{2}_\d{2}_\d{4}'  # Format: 29_10_2022
    # ]
    #
    # for item in cq_tabcontent:
    #     aaa = item.find_all('a')
    #     for url__ in aaa:
    #         url_ = url__.get('href')
    #
    #         pattern = r'https?://[^\s]+\.xlsx'
    #
    #         if re.findall(pattern, url_):
    #             arr_.append(url_)
    #
    #             for date_pattern in date_patterns:
    #                 match = re.search(date_pattern, url_)
    #                 if match:
    #                     date = match.group(0)
    #                     # date = date.replace('-', '').replace('.', '')
    #                     date = date.replace('-', '').replace('.', '').replace('_', '')
    #
    #                     try:
    #                         date_object = dt.strptime(date, "%d%m%Y")
    #                     except ValueError:
    #                         date_object = dt.strptime(date, "%d%m-%Y")
    #
    #                     formatted_date = date_object.strftime("%Y%m%d")
    #
    #             file_date = dt.strptime(formatted_date, "%Y%m%d").date()
    #
    #             if start <= file_date <= stop:
    #                 response = requests.get(url_, headers=headers)
    #
    #                 filename = f'{formatted_date}.xlsx'
    #
    #                 if not os.path.exists(filename):
    #                     with open(filename, "wb") as file:
    #                         file.write(response.content)
    #                     print(f"File: {filename} >>> downloaded successfully.")
    #                 else:
    #                     print(f"File: {filename} >>> already exists. Skipped.")

    file_list = os.listdir(folder_path)

    xlsx_files = [file for file in file_list if file.endswith('.xlsx')]

    # Sort files by name
    sorted_files = sorted(xlsx_files)

    # Function to extract date from filename
    def extract_date(filename):
        return pd.to_datetime(filename.split('.')[0], format='%Y%m%d')

    # Sort files by date using function extract_date
    sorted_files = sorted(sorted_files, key=extract_date)

    data = {}  # Dictionary to store data from all files

    # Reading Files Sequentially
    for file in sorted_files:
        # print(f'file: {file}')
        file_path = os.path.join(folder_path, file)
        file_name = os.path.basename(file_path)

        date_match = re.search(r'\d{8}', file_name)
        if date_match:
            date_str = date_match.group(0)
            date_obj = datetime.datetime.strptime(date_str, "%Y%m%d")
            formatted_date = date_obj.strftime("%Y-%m-%d")
        else:
            print("Date not found in filename!")

        workbook = openpyxl.load_workbook(file_path)

        for sheet in workbook.sheetnames:
            current_sheet = workbook[sheet]

            # print(f'current_sheet: {current_sheet}')

            sheet_name = translit(sheet.replace('ї', 'и'), language_code='ru', reversed=True)
            sheet = sheet_name.replace("'", "").replace(">>", "_")
            # print(f'sheet: {sheet}')

            if sheet not in data:
                data[sheet] = []

            if "SKASOVANO" in sheet:
                print(">>>>> 'SKASOVANO' <<<<< !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            else:
                sheet_data = []

                for row in range(4, 28):

                    cell_B = current_sheet['B' + str(row)].value
                    cell_C = current_sheet['C' + str(row)].value
                    cell_D = current_sheet['D' + str(row)].value
                    cell_E = current_sheet['E' + str(row)].value

                    # print(f'cell_B: {cell_B}')

                    if cell_B is None:

                        # Creating a set of all available hours
                        existing_hours = set(
                            timestamp.split(' ')[1].split(':')[0] for data_item in sheet_data for timestamp in
                            [data_item['timestamp']]
                        )
                        # Creating the set of all possible hours in a day
                        all_hours = set(str(i).zfill(2) for i in range(0, 24))
                        # Definition of a missed hour
                        missing_hour = all_hours.difference(existing_hours).pop()

                        # target_timestamp = f'2023-03-26 {missing_hour}:00:00'
                        replacement_timestamp = f'2023-03-26 {str(int(missing_hour) + 1).zfill(2)}:00:00'


                        # Find index of entry with specified timestamp
                        index = next((index for index, item in enumerate(sheet_data) if
                                      item['timestamp'] == replacement_timestamp), None)

                        if index is not None:
                            # Get values from found record
                            c_value = sheet_data[index]['C']
                            d_value = sheet_data[index]['D']
                            e_value = sheet_data[index]['E']

                            # Create a new dictionary insert_data
                            insert_data = {'timestamp': '2023-03-26 03:00:00', 'C': c_value, 'D': d_value, 'E': e_value}

                        # Find index of timestamp before which to insert data
                        indexxx = next((index for index, item in enumerate(sheet_data) if
                                        item['timestamp'] == '2023-03-26 04:00:00'), None)

                        if indexxx is not None:
                            # Insert data before specified index
                            sheet_data.insert(indexxx, insert_data)

                    else:
                        ts = f"{int(cell_B) - 1:02d}:00:00"
                        hour_ = f'{formatted_date} {ts}'

                        sheet_data.append({
                            'timestamp': hour_,
                            'C': cell_C,
                            'D': cell_D,
                            'E': cell_E
                        })

                data[sheet].extend(sheet_data)

    csv_files = []

    # Saving data to a file CSV
    for sheet_name, sheet_data in data.items():
        # file_name_json = f'{sheet_name}.json'
        file_name_csv = f'{sheet_name}.csv'

        try:
            headers = list(sheet_data[0].keys())

            csv_files.append(sheet_name)

            with open(file_name_csv, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(sheet_data)

            # print(f"CSV-файл: '{file_name_csv}' >>> successfully created.")
        except:
            pass

    columns = ['timestamp']
    for file_ in csv_files:
        file_name = f'{file_}.csv'
        columns.append(file_name[:-4] + ' PX')
        columns.append(file_name[:-4] + ' NTC')
        columns.append(file_name[:-4] + ' AC')

    data = {}

    for file_ in csv_files:
        file_name = f'{file_}.csv'
        try:
            with open(file_name, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Header Skip
                for row in reader:
                    timestamp = row[0]
                    if timestamp not in data:
                        # If the key is missing, create a new entry in the dictionary
                        data[timestamp] = {}
                    # Fill in data for each column
                    data[timestamp][file_name[:-4] + ' PX'] = row[1]
                    data[timestamp][file_name[:-4] + ' NTC'] = row[2]
                    data[timestamp][file_name[:-4] + ' AC'] = row[3]
        except:
            pass

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # Title entry
        for timestamp in sorted(data.keys()):
            row = [timestamp]
            for column in columns[1:]:
                if column in data[timestamp]:
                    row.append(data[timestamp][column])
                else:
                    row.append(0)
            writer.writerow(row)


if __name__ == "__main__":
    get_ua_data(start, stop, folder_path)