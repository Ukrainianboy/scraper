# -*- coding: utf-8 -*-
import requests
from lxml import html
import csv


def get_response(url):
    session = requests.Session()
    request = session.get(url)
    return request


def get_urls(request):
    hrefs = []
    parsed_body = html.fromstring(request.content)
    elements = parsed_body.find_class('eInfo')
    for element in elements:
        for href in element.findall('.//a'):
            x = href.get('href')
            if not x.startswith('javascript'):
                hrefs.append('https://www.vivaness.de'+str(x))
    return hrefs


def get_info(hrefs):
    data_for_csv = []
    for url in hrefs:
        session = requests.Session()
        request = session.get(url)
        body = html.fromstring(request.content)
        name = body.xpath('//*[@id="maintop"]/div/div[3]/h1/span')  # company_name
        if name:
            name = name[0].text.strip()
        site = body.xpath('//*[@id="maintop"]/div/div[3]/div[2]/div[1]/p/a')  # site
        if site:
            site = site[0].text.strip()
        print(name, site)
        data = [name, site]
        data_for_csv.append(data)
    return data_for_csv


def write_data(data_for_csv):
    with open('parser.csv', 'a') as f:
        writer = csv.writer(f, delimiter=',')
        for data in data_for_csv:
            writer.writerow(data)


def make_all(url_adr):
    url = get_response(url_adr)
    urls = get_urls(url)
    info = get_info(urls)
    write_data(info)


if __name__ == '__main__':
    make_all('https://www.vivaness.de/de/ausstellerprodukte/exhibitorlist?edbid=viva18&filterchar=*&items=261')

