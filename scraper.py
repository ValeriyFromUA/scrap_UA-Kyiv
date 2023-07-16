import os
import re
from typing import Dict, List, NoReturn
from urllib import request

from bs4 import BeautifulSoup

from db.database import get_session
from db.models.clients import Client
from logger import get_logger

logger = get_logger(__name__)
session = get_session()


def open_text_file(file_name: str) -> List[str]:
    with open(file_name, 'r') as file:
        lines = file.readlines()
        return lines


def save_main_page(url: str) -> NoReturn:
    response = request.urlopen(url)
    html = response.read()
    html = str(html)
    with open('test_page.html', 'w') as file:
        file.write(str(html))
        logger.info(f'Template file was created for: {url}')


def clean_trash() -> NoReturn:
    if os.path.exists('test_page.html'):
        os.remove('test_page.html')
        os.remove('links.txt')
        logger.info("Files 'test_page.html' and 'links.txt' was deleted.")
    else:
        logger.info("Files 'test_page.html' and 'links.txt' not exist")


def find_links_on_page(url: str) -> int:
    data = []
    response = request.urlopen(url)
    page = response.read()
    soup = BeautifulSoup(page, 'html.parser')
    links = soup.find_all(class_='row p-3 p-md-4')
    for link in links:
        link_element = link.find('a')
        href = link_element['href']
        data.append(href)
    data = list(set(data))
    with open('links.txt', 'a') as file:
        for line in data:
            file.write(f'https://www.ua-region.com.ua{line}\n')

    return len(links)


def find_all_links(first_page: int, last_page: int) -> NoReturn:
    count = 0
    for number in range(first_page, last_page + 1):
        count += find_links_on_page(f'https://www.ua-region.com.ua/ter/8000000?start_page={number}')
        logger.info(f"{count} links was saved...")


def find_data_in_link(url: str) -> Dict:
    response = request.urlopen(url)
    page = response.read()
    soup = BeautifulSoup(page, 'html.parser')
    try:
        company_type = soup.find('h1').text.split(',')[1]
    except:
        company_type = ''
    phones = soup.find_all(class_='ui-link')
    phones = list(set([phone['href'].strip('tel:') for phone in phones if '+380' in phone['href']]))
    links = soup.find_all('a')
    emails = list(set([email['href'].split(':')[1] for email in links if '@' in email['href']]))
    emails.remove('info@ua-region.com')
    web = None
    for link in links:
        if 'https:' in link.text:
            web = link.text
            break
    description = soup.find(class_='hide_text').text if soup.find(class_='hide_text') else ''
    activity = soup.find(class_='ui-list-mark-2 list-unstyled').text if soup.find(
        class_='ui-list-mark-2 list-unstyled') else ''
    activity_list = re.split(r"(?<=\w)(?=[А-ЯЁ])", activity)
    return {
        'name': soup.find('h1').text.split(',')[0],
        'type': company_type,
        'activity': activity_list,
        'address': soup.find(class_='company-sidebar__data').text if soup.find(class_='company-sidebar__data') else '',
        'phones': phones,
        'emails': emails,
        'url': web,
        'description': description
    }


def collect_data(link_list: List) -> List[Dict]:
    count = 1
    collected_data = []
    for link in link_list:
        if link not in collected_data:
            collected_data.append(find_data_in_link(link))
            logger.info(f"{count} page(s) with data was saved...")
            count += 1
    logger.info("All data was saved, you can save data to DB now...")
    return collected_data


def save_data_to_db(data_list: List[Dict]):
    count = 1
    clients = []

    for data in data_list:
        client = Client(
            name=data['name'],
            type=data['type'],
            activity=data['activity'],
            address=data['address'],
            phone=data['phones'],
            email=data['emails'],
            url=data['url'],
            description=data['description'],
        )
        clients.append(client)
        logger.info(f"added {count} records for saving")
        count += 1
    logger.info("Start: saving data to DB")
    session.add_all(clients)
    session.commit()
    logger.info("All data was saved to DB")
