from bs4 import BeautifulSoup


with open("urlsss.html") as file:
    soup = BeautifulSoup(file, "html.parser")

a_tags = soup.find_all("a")

xlsx_links = [a['href'] for a in a_tags if a.get('href', '').endswith('.xlsx')]

with open("urlsss.txt", "w") as outfile:
    for link in xlsx_links:
        outfile.write(link + "\n")
