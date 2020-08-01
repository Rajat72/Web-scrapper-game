from bs4 import BeautifulSoup
import requests
from time import sleep
from csv import DictWriter


def scrap():
    all_q = []
    base = "http://quotes.toscrape.com"
    url = "/page/1"
    while url:
        res = requests.get(f"{base}{url}")
        print(f"now scrapping {base}{url}....")
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.find_all(class_="quote")
        for quote in quotes:
            all_q.append({
                "txt": quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "bio": quote.find("a")["href"]})
        next_button = soup.find(class_="next")
        url = next_button.find("a")["href"] if next_button else None
        # sleep(2)
    return all_q


QOUTE = scrap()
with open("quotes.csv", "w") as file:
    headers = ["txt", "author", "bio"]
    csv_writer = DictWriter(file, fieldnames=headers)
    csv_writer.writeheader()
    for quote in QOUTE:
        csv_writer.writerow(quote)
