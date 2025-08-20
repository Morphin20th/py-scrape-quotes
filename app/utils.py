import csv
from dataclasses import astuple
from typing import Callable

import requests
from bs4 import Tag, BeautifulSoup

BASE_URL = "https://quotes.toscrape.com/"


def get_first_page_soup() -> BeautifulSoup:
    text = requests.get(BASE_URL).content
    return BeautifulSoup(text, "html.parser")


def is_next_page(soup: Tag) -> bool:
    next_page = soup.select(".next")
    if not next_page:
        return False
    return True


def write_quotes_to_csv(elements: list, path: str, fields: list) -> None:
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerows([astuple(element) for element in elements])


def get_all_items(parse_func: Callable[[BeautifulSoup], list]) -> list:
    first_page_soup = get_first_page_soup()
    items = parse_func(first_page_soup)

    i = 1
    while True:
        i += 1
        text = requests.get(f"{BASE_URL}page/{i}").content
        next_page_soup = BeautifulSoup(text, "html.parser")
        items.extend(parse_func(next_page_soup))
        if not is_next_page(next_page_soup):
            break
    return items
