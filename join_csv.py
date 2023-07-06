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
                row.append('0')
        writer.writerow(row)
