import urllib3
import requests
import pandas as pd
import time
import os
from tqdm import tqdm

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

urllib3.disable_warnings()

df = pd.read_csv('/tmp/model_url_list.csv', header=None)
model_url_list = df[0].tolist()

api_url_list = []
for i in model_url_list:
    api_url_list.append(i.replace('https://grabcad.com/library/', 'https://grabcad.com/community/api/v1/models/'))

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"}
cookies = {"_grabcad_session": "b303bdccc0b1a832d013174888203747"}

archive_url_list = []
session = requests.Session()
for api_url in tqdm(api_url_list, desc="Fetching archive URLs"):
    # retry = Retry(connect=3, backoff_factor=0.5)
    # adapter = HTTPAdapter(max_retries=retry)
    # session.mount('http://grabcad.com', adapter)
    # session.mount('https://grabcad.com', adapter)
    response = session.get(api_url, cookies=cookies, headers=headers, verify=False)
    if response.json().get('archive_url') is not None:
        archive_url_list.append(response.json()['archive_url'])

os.makedirs('/tmp', exist_ok=True)
pd.DataFrame(archive_url_list).to_csv('/tmp/archive_url_list.csv', index=False, header=False)