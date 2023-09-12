from urllib.parse import urlencode
import requests
from tqdm.notebook import tqdm
from bs4 import BeautifulSoup
import typing as tp
import time

API_KEY = 'bc467b9b-a5ee-409d-9f82-9563006e4b2e'

def get_page_content(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    r = requests.get(proxy_url)
    return BeautifulSoup(r.content, 'html.parser')

def get_hrefs(tree):
    aparts = tree.find_all('div', {'class': '_93444fe79c--general--BCXJ4'})
    result = []
    for apart in aparts:
        result.append({
            'href': apart.div.a.get('href'),
            'title': apart.div.div.span.text[0:],
        })

    return result

data = []
for i in tqdm(range(1, 4)):
    url = f'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={i}&region=1'
    tree = get_page_content(url)
    aparts = get_hrefs(tree)
    data.extend(aparts)
    time.sleep(0.1)

import pandas as pd
df = pd.DataFrame(data)
df

def get_apart_info(apart_info):
    href = f'{apart_info["href"]}'
    tree = get_page_content(href)
    price=tree.find('span', {'style': 'letter-spacing:-0.5px'})
    area=tree.find('span',{'style':'letter-spacing:-0.2px'})
    apart_info.update({'area':area})
    apart_info.update({'price':price})
    return apart_info

new_data = []

for item in tqdm(data[:10]):
    new_data.append(get_apart_info(item))

updated_df = pd.DataFrame(new_data)
updated_df