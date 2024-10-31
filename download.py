import pandas as pd
import requests

df = pd.read_csv('archive_url_list.csv', header=None)
archive_url_list = df[0].tolist()

download_url_list = []
model_index = 1
session = requests.Session()
for i in archive_url_list:
    download_url = 'https://d2t1xqejof9utc.cloudfront.net/cads/files/' + i.partition('=')[-1] + '/original.zip'
    file_path = 'E:\\grabcad\\{}.zip'.format(str(model_index).zfill(4))
    response = session.get(download_url)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    download_url_list.append(download_url)
    model_index += 1

pd.DataFrame(download_url_list).to_csv('download_url_list.csv', index=False, header=False)
