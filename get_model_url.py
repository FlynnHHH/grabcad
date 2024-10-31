# Description: This script scrapes the GrabCAD website for sheet metal models and saves the URLs to a CSV file.
import time
import pandas as pd

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

model_url_list = []

for page_index in range(1, 3):
    website='https://grabcad.com/library?page={}&per_page=100&time=all_time&sort=recent&query=sheet%20metal'.format(*str(page_index))
    
    options = Options()
    options.add_argument('--log-level=3')
    wd = webdriver.Chrome(options=options)
    wd.get(website)

    WebDriverWait(wd, 30).until(EC.visibility_of_all_elements_located((By.XPATH, "//span[@class='text ng-binding']")))
    model_url = wd.find_elements(By.CLASS_NAME, 'modelLink')
    for i in model_url:
        model_url_list.append(i.get_attribute('href'))
    
    time.sleep(3)    
    wd.quit()
    print('End of page', page_index)

pd.DataFrame(model_url_list).to_csv('model_url_list.test.csv', index=False, header=False)
print('Data saved to grabcad_library.csv')
