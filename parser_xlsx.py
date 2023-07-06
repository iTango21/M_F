import os
import re
import datetime
import json
import pandas as pd
import csv
import openpyxl
from transliterate import translit

# Замените на свой путь!
folder_path = 'D:\\_work_2023_\\programming\\Python\\0 _ freelance _ 0\\upw\\M_F\\'


file_list = os.listdir(folder_path)

xlsx_files = [file for file in file_list if file.endswith('.xlsx')]

# Сортировка файлов по имени
sorted_files = sorted(xlsx_files)

# Функция для извлечения даты из имени файла
def extract_date(filename):
    return pd.to_datetime(filename.split('.')[0], format='%Y%m%d')

# Сортировка файлов по дате с использованием функции extract_date
sorted_files = sorted(sorted_files, key=extract_date)

data = {}  # Словарь для хранения данных из всех файлов

# Чтение файлов последовательно
for file in sorted_files:
    file_path = os.path.join(folder_path, file)
    file_name = os.path.basename(file_path)

    date_match = re.search(r'\d{8}', file_name)
    if date_match:
        date_str = date_match.group(0)
        date_obj = datetime.datetime.strptime(date_str, "%Y%m%d")
        formatted_date = date_obj.strftime("%Y-%m-%d")
    else:
        print("Дата не найдена в имени файла!")

    workbook = openpyxl.load_workbook(file_path)

    for sheet in workbook.sheetnames:
        current_sheet = workbook[sheet]

        sheet_name = translit(sheet.replace('ї', 'и'), language_code='ru', reversed=True)
        sheet = sheet_name.replace("'", "").replace(">>", "_")

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

                ts = f"{int(cell_B) - 1:02d}:00:00"
                hour_ = f'{formatted_date} {ts}'

                sheet_data.append({
                    'timestamp': hour_,
                    'C': cell_C,
                    'D': cell_D,
                    'E': cell_E
                })

            data[sheet].extend(sheet_data)

# Сохранение данных в файлы JSON и CSV
for sheet_name, sheet_data in data.items():
    file_name_json = f'{sheet_name}.json'
    file_name_csv = f'{sheet_name}.csv'

    with open(file_name_json, 'w', encoding='utf-8') as file:
        json.dump(sheet_data, file, ensure_ascii=False, indent=4)
        print(f"JSON-файл: {file_name_json} >>> successfully created.")

    headers = list(sheet_data[0].keys())

    with open(file_name_csv, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(sheet_data)

    print(f"CSV-файл: '{file_name_csv}' >>> successfully created.")
