import requests
from bs4 import BeautifulSoup

html = requests.get("https://ru.wikipedia.org/wiki/Зелёный_слоник").text
bs4 = BeautifulSoup(html, "html.parser")
print(*(t.get('title') for t in bs4.select('table td a[title]')), sep='\n')
