import requests
import re
from datetime import datetime

date_pattern = r"(\d{2}\.\d{2}\.\d{4})"
urls_file = "urlsss.txt"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

with open(urls_file, "r") as file:
    links = file.readlines()

for link in links:
    link = link.strip()
    match = re.search(date_pattern, link)
    if match:
        date_str = match.group(1)
        date_obj = datetime.strptime(date_str, "%d.%m.%Y")
        date_str = date_obj.date().isoformat()  # 2022-12-02

        formatted_date = datetime.strftime(date_obj, "%Y%m%d")  # 20221202
        # print(formatted_date)

        url = link
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        filename = f'{formatted_date}.xlsx'

        with open(filename, "wb") as file:
            file.write(response.content)

        print(f"File: {filename} >>> downloaded successfully.")
