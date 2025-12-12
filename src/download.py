import pandas as pd
import requests
import os
from tqdm import tqdm

df = pd.read_csv('/tmp/archive_url_list.csv', header=None)
archive_url_list = df[0].tolist()

download_url_list = []
model_index = 1
session = requests.Session()

# Create download directory if it doesn't exist
download_dir = 'E:/dataset/grabcad_plane'
os.makedirs(download_dir, exist_ok=True)

for i in tqdm(archive_url_list, desc="Downloading models"):
    download_url = 'https://d2t1xqejof9utc.cloudfront.net/cads/files/' + i.partition('=')[-1] + '/original.zip'
    file_path = os.path.join(download_dir, '{}.zip'.format(str(model_index).zfill(4)))
    response = session.get(download_url)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    download_url_list.append(download_url)
    model_index += 1

os.makedirs('/tmp', exist_ok=True)
pd.DataFrame(download_url_list).to_csv('/tmp/download_url_list.csv', index=False, header=False)
