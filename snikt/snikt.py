import requests
import sys
import os
import re
from bs4 import BeautifulSoup


def clean_for_url(plain_text):
    return re.sub(r'[^A-Za-z\d]+', '-', plain_text).strip('-')


def scrape_book_details(book):
    title = book.find('div', class_='lv2-micro-item-title').get_text().strip()
    issue = book.find('div', class_='lv2-micro-item-subtitle').get_text().strip()
    link = book.find('a')['href']
    id_num = link[link.rfind('/'):][1:]
    store_link = f'https://www.comixology.eu/{clean_for_url(title)}-{clean_for_url(issue)}/digital-comic/{id_num}'
    #TODO scrape the store link to get the credits


def scrape(library_html_file_names):
    for library_html_file_name in library_html_file_names:
        with open(f'{os.getcwd()}/../{library_html_file_name}', 'r') as library_html_file:
            soup = BeautifulSoup(library_html_file, 'html.parser')
            for book in soup.find_all('li', class_='lv2-book-micro-item'):
                scrape_book_details(book)
                break


if __name__ == '__main__':
    scrape(sys.argv[1:])