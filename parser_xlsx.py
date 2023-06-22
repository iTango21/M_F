import os
import re
import datetime
import json
import pandas as pd
import csv
import openpyxl
from transliterate import translit


# ATTENTION! Replace with your own way!
# Folder containing .xlsx files
# folder_path = 'D:\\_work_\\programming\\Python\\0 _ freelance _ 0\\upw\\M_F\\'
folder_path = 'D:\\_work_2023_\\programming\\Python\\0 _ freelance _ 0\\upw\\M_F\\'

file_list = os.listdir(folder_path)

xlsx_files = [file for file in file_list if file.endswith('.xlsx')]

# print(len(xlsx_files))
# breakpoint()

# Sort files by name
sorted_files = sorted(xlsx_files)

# Function to extract date from filename
def extract_date(filename):
    return pd.to_datetime(filename.split('.')[0], format='%Y%m%d')

# Sort files by date using the extract_date function
sorted_files = sorted(sorted_files, key=extract_date)

# Чтение файлов последовательно
for file in sorted_files:
    file_path = os.path.join(folder_path, file)

    # file_path = r"D:\_work_\programming\Python\0_ freelance _ 0\upw\M_F\20220501.xlsx"
    file_name = os.path.basename(file_path)

    date_match = re.search(r'\d{8}', file_name)
    if date_match:
        date_str = date_match.group(0)
        date_obj = datetime.datetime.strptime(date_str, "%Y%m%d")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        print(formatted_date)
    else:
        print("The date was not found in the file name!")

    workbook = openpyxl.load_workbook(file_path)

    unique_sheet = []
    data = {}

    for sheet in workbook.sheetnames:

        current_sheet = workbook[sheet]

        sheet_name = translit(sheet.replace('ї', 'и'), language_code='ru', reversed=True)
        sheet = sheet_name.replace("'", "").replace(">>", "_")
        # print(sheet)

        if "SKASOVANO" in sheet:
            print(">>>>> 'SKASOVANO' <<<<< !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        else:
            if sheet not in unique_sheet:
                unique_sheet.append(sheet)

            sheet_data = []

            for row in range(4, 28):
                # Get the values of cells C, D, E for the current row
                cell_B = current_sheet['B' + str(row)].value
                cell_C = current_sheet['C' + str(row)].value
                cell_D = current_sheet['D' + str(row)].value
                cell_E = current_sheet['E' + str(row)].value
                # print(f'BBB: {cell_B}')

                ts = f"{int(cell_B) - 1:02d}:00:00"
                # print(ts)
                hour_ = f'{formatted_date} {ts}'

                sheet_data.append(
                    {
                        'timestamp': hour_,
                        'C': cell_C,
                        'D': cell_D,
                        'E': cell_E
                    }
                )

            data[sheet] = sheet_data

for i in data:
    file_name_json = f'{i}.json'
    file_name_csv = f'{i}.csv'

    with open(file_name_json, 'w', encoding='utf-8') as file:
        json.dump(data[i], file, ensure_ascii=False, indent=4)
        print(f"JSON-file: {file_name_json} >>> successfully created.")

    with open(file_name_json, 'r') as f:
        dataaa = json.load(f)

    headers = list(dataaa[0].keys())

    with open(file_name_csv, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(dataaa)

    print(f"CSV-file: '{file_name_csv}' >>> successfully created.")
