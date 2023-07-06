import csv
from datetime import datetime, timedelta

# Определяем временной диапазон
start_time = datetime(2022, 4, 30, 21, 0)
end_time = datetime(2023, 5, 31, 20, 0)
total_hours = int((end_time - start_time).total_seconds() / 3600) + 1

# Создаем новый файл
output_file = 'join_csv_new.csv'
with open('join_csv.csv', 'r') as f_in, open(output_file, 'w', newline='') as f_out:
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)

    # Записываем заголовок с добавленным столбцом "index"
    header = next(reader)
    header_with_index = ['index'] + header
    writer.writerow(header_with_index)

    # Создаем и записываем строки с временными метками (Unix Time Stamp), индексами и исходными данными
    for i, row in enumerate(reader, start=1):
        timestamp = start_time + timedelta(hours=i-1)
        unix_timestamp = int(timestamp.timestamp())
        row_with_index = [unix_timestamp] + row
        writer.writerow(row_with_index)

# Проверяем наличие всех дат в данных
existing_dates = set()
with open('join_csv.csv', 'r') as f_in:
    reader = csv.reader(f_in)
    next(reader)  # Пропускаем заголовок
    for row in reader:
        timestamp = row[0]
        existing_dates.add(timestamp.split()[0])  # Добавляем только дату без времени

date_range = set()
current_date = start_time.date()
while current_date <= end_time.date():
    date_range.add(str(current_date))
    current_date += timedelta(days=1)

missing_dates = date_range - existing_dates
if missing_dates:
    print(f'\nThe following dates are missing from the data:')
    for date in missing_dates:
        print(date)
else:
    print('All dates are present in the data.')
