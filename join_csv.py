import csv

csv_files = ['HAES (Ukraina)_Zheshuv (Polscha).csv', 'Moldova_Ukraina.csv', 'Rumunіja_Ukraina.csv', 'Slovachchina_Ukraina.csv', 'Ugorschina_Ukraina.csv', 'Ukraina_Moldova.csv', 'Ukraina_Polscha.csv', 'Ukraina_Rumunіja.csv', 'Ukraina_Slovachchina.csv', 'Ukraina_Slovachchina35.csv', 'Ukraina_Ugorschina.csv', 'Zheshuv (Polscha)_HAES (Ukraina).csv']
output_file = 'join_csv.csv'

# Создание списка имен столбцов
columns = ['timestamp']
for file_name in csv_files:
    columns.append(file_name[:-4] + ' PX')
    columns.append(file_name[:-4] + ' NTC')
    columns.append(file_name[:-4] + ' AC')

# Создание пустого словаря для хранения данных
data = {}

# Итерация по файлам CSV
for file_name in csv_files:
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Пропуск заголовка
        for row in reader:
            timestamp = row[0]
            if timestamp not in data:
                # Если ключ отсутствует, создаем новую запись в словаре
                data[timestamp] = {}
            # Заполняем данные для каждого столбца
            data[timestamp][file_name[:-4] + ' PX'] = row[1]
            data[timestamp][file_name[:-4] + ' NTC'] = row[2]
            data[timestamp][file_name[:-4] + ' AC'] = row[3]

# Запись данных в файл CSV
with open(output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(columns)  # Запись заголовка
    for timestamp in sorted(data.keys()):
        row = [timestamp]
        for column in columns[1:]:
            if column in data[timestamp]:
                row.append(data[timestamp][column])
            else:
                row.append('***')
        writer.writerow(row)


breakpoint()

























import csv

csv_files = [
    'HAES (Ukraina)_Zheshuv (Polscha).csv',
    'Moldova_Ukraina.csv',
    'Rumunіja_Ukraina.csv',
    'Slovachchina_Ukraina.csv',
    'Ugorschina_Ukraina.csv',
    'Ukraina_Moldova.csv',
    'Ukraina_Polscha.csv',
    'Ukraina_Rumunіja.csv',
    'Ukraina_Slovachchina.csv',
    'Ukraina_Slovachchina35.csv',
    'Ukraina_Ugorschina.csv',
    'Zheshuv (Polscha)_HAES (Ukraina).csv'
]

output_file = 'join_csv.csv'

# Составляем список уникальных ключей на основе значений в столбце "timestamp"
unique_keys = []
for file in csv_files:
    with open(file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Пропускаем заголовок
        for row in reader:
            key = row[0]
            if key not in unique_keys:
                unique_keys.append(key)

# Создаем заголовки столбцов для выходного CSV-файла
header = ['timestamp']
for file in csv_files:
    base_name = file.split('.')[0]
    header.append(base_name + ' PX')
    header.append(base_name + ' NTC')
    header.append(base_name + ' AC')

# Создаем и заполняем данные для выходного CSV-файла
data = []
for key in unique_keys:
    row = [key]
    for file in csv_files:
        with open(file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Пропускаем заголовок
            for row in reader:
                if row[0] == key:
                    row.append(row[1])
                    row.append(row[2])
                    row.append(row[3])
                    break
            else:
                row.append('***')
                row.append('***')
                row.append('***')
    data.append(row)

# Записываем данные в выходной CSV-файл
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(data)
















#
# # Создание пустого DataFrame для объединения данных
# combined_data = pd.DataFrame(columns=['timestamp'])
#
# # Цикл по каждому CSV-файлу
# for file in csv_files:
#     # Чтение текущего файла CSV
#     data = pd.read_csv(file)
#
#     # Извлечение имени столбца из имени файла
#     column_name = file[:-4]  # Удаляем расширение ".csv"
#     column_name = column_name.replace(' (', '_').replace(')', '').replace(' ', '_')
#
#     # Проверка наличия столбцов "C", "D" и "E"
#     if 'C' in data.columns and 'D' in data.columns and 'E' in data.columns:
#         # Создание новых столбцов для текущего файла
#         combined_data[column_name + '_PX'] = data['C']
#         combined_data[column_name + '_NTC'] = data['D']
#         combined_data[column_name + '_AC'] = data['E']
#     else:
#         # Если столбцы отсутствуют, заполнить значениями "***"
#         combined_data[column_name + '_PX'] = '***'
#         combined_data[column_name + '_NTC'] = '***'
#         combined_data[column_name + '_AC'] = '***'
#
# # Запись объединенных данных в CSV-файл
# combined_data.to_csv('join_csv.csv', index=False)
