import requests
import sys
import os
import re
from bs4 import BeautifulSoup


def clean_for_url(plain_text):
    return re.sub(r'[^A-Za-z\d]+', '-', plain_text).strip('-')


def scrape_book_in_store_page(store_url):
    book_in_store_page = requests.get(store_url)
    book_credits = dict()
    if book_in_store_page.status_code == 200:
        soup = BeautifulSoup(book_in_store_page.text, 'html.parser')
        credits = soup.find('div', class_='credits')
        for credit in credits.find_all('dl'):
            type = credit.find('dt').get_text().strip()
            for person in credit.find_all('a'):
                people = book_credits.get(type, list())
                person_name = person.get_text().strip()
                if person_name not in ['More...', 'HIDE...']:
                    people.append(person.get_text().strip())
                    book_credits[type] = people
    else:
        raise ValueError(f'{store_url} response: {book_in_store_page.status_code}')
    return book_credits


def scrape_book_details(book):
    title = book.find('div', class_='lv2-micro-item-title').get_text().strip()
    issue = book.find('div', class_='lv2-micro-item-subtitle').get_text().strip()
    link = book.find('a')['href']
    id_num = link[link.rfind('/'):][1:]
    store_link = f'https://www.comixology.eu/{clean_for_url(title)}-{clean_for_url(issue)}/digital-comic/{id_num}'
    credits = scrape_book_in_store_page(store_link)
    print(f'Title: {title}\nIssue: {issue}\nCredits: {credits}\n\n')


def scrape(library_html_file_names):
    count = 3
    for library_html_file_name in library_html_file_names:
        with open(f'{os.getcwd()}/../{library_html_file_name}', 'r') as library_html_file:
            soup = BeautifulSoup(library_html_file, 'html.parser')
            for book in soup.find_all('li', class_='lv2-book-micro-item'):
                scrape_book_details(book)
                count = count - 1
                if count < 0:
                    break


if __name__ == '__main__':
    scrape(sys.argv[1:])
    #dets = scrape_book_in_store_page('https://www.comixology.eu/Inception-The-Cobol-Job/digital-comic/2853')
    #dets = scrape_book_in_store_page('https://www.comixology.eu/Infinite-Frontier-2021-0/digital-comic/921913')
    #print(dets)