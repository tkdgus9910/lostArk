# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 17:08:23 2024

@author: tmlab
"""


from selenium import webdriver # selenium의 webdriver를 사용하기 위한 import
from selenium.webdriver.common.keys import Keys # selenium으로 키를 조작하기 위한 import

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_recaptcha_solver import RecaptchaSolver


test_ua = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2050.0 Safari/537.36'
download_dir = "D:\paper"  # 다운로드 받을 경로 설정
download_dir = "D:\conference_paper"  # 다운로드 받을 경로 설정
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument(f'--user-agent={test_ua}')

options.add_argument('--no-sandbox')
options.add_argument("--disable-extensions")

# 자동 다운로드 설정
prefs = {
    "download.default_directory": download_dir,  # 다운로드 경로 설정
    "download.prompt_for_download": False,       # 다운로드 팝업 끄기
    "directory_upgrade": True,                   
    # "safebrowsing.enabled": T1rue                 # 안전 탐색 켜기
}

options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(executable_path='D:/github/chromedriver-win64/chromedriver.exe'
                           ,chrome_options= options)

#%%

url = f"https://loawa.com/stat/seal"

# url = ""
driver.get(url)

#%% 직업 리스트
job_list = driver.find_elements(By.XPATH, '//*[@name="jobs"]') # 시간 필요    
job_text_list = [i.get_attribute("value") for i in job_list]

#%% 직업 클릭
Job = job_text_list[1]

# value 속성이 'job'인 요소 클릭
element = driver.find_element(By.XPATH, f'//span[text()="{Job}"]')
element.click()

#%% 유효 레벨 조정

element = driver.find_element(By.XPATH, '//*[@id="pages-statics-seal"]/div[2]/div[1]/form/div/div/div[7]/div/div[2]/div/input[3]')
element.clear()

query = '1680'
element.send_keys(query)

xpath = '//*[@id="pages-statics-seal"]/div[2]/div[1]/form/div/div/div[7]/div/div[2]/div/button'
element = driver.find_element(By.XPATH, xpath).click() # 적용
time.sleep(5)


#%% 각인 클릭

element = driver.find_element(By.XPATH, '//*[@id="seal-list-start"]/div[1]/div/div[2]/ul/li[1]/div[1]/div')
Seal = element.text.split('\n')[0]
element.click()


#%% 각인 채용률 리스트
import pandas as pd 

result_df = pd.DataFrame()

for i in range(1,21):
    
    xpath = f'//*[@id="seal-list-start"]/div[2]/div/div[2]/ul/li[{i}]/div[1]/div/h4'
    element = driver.find_element(By.XPATH, xpath)
    texts = element.text
    
    Seal_name = texts.split('\n')[0]
    Seal_ratio = texts.split('| ')[-1]
    temp = pd.DataFrame({'직업' : [Job], 
                         '직업각인' : [Seal], 
                         '공통각인' : [Seal_name], 
                         '공통각인 비중' : [Seal_ratio]
                         })
    result_df = pd.concat([result_df, temp] , axis = 0)
    

# //*[@id="seal-list-start"]/div[2]/div/div[2]/ul/li[2]/div[1]/div/h4


#%% 전체 과정 반복

job_list = driver.find_elements(By.XPATH, '//*[@name="jobs"]') # 시간 필요    
job_text_list = [i.get_attribute("value") for i in job_list]

#%% 유효 레벨 조정

element = driver.find_element(By.XPATH, '//*[@id="pages-statics-seal"]/div[2]/div[1]/form/div/div/div[7]/div/div[2]/div/input[3]')
element.clear()

query = '1680'
element.send_keys(query)

xpath = '//*[@id="pages-statics-seal"]/div[2]/div[1]/form/div/div/div[7]/div/div[2]/div/button'
element = driver.find_element(By.XPATH, xpath).click() # 적용
time.sleep(5)

#%% 직업 클릭
import pandas as pd 

result_df = pd.DataFrame()

for Job in job_text_list :

    # value 속성이 'job'인 요소 클릭
    element = driver.find_element(By.XPATH, f'//span[text()="{Job}"]')
    element.click()
    time.sleep(5)
    
    # 각인 클릭
    for s in [1, 2]: 
        element = driver.find_element(By.XPATH, f'//*[@id="seal-list-start"]/div[1]/div/div[2]/ul/li[{s}]/div[1]/div')
        Seal = element.text.split('\n')[0]
        element.click()
        time.sleep(5)
        
        
        # 각인 채용률 리스트
        for i in range(1,21):
            
            try : 
                xpath = f'//*[@id="seal-list-start"]/div[2]/div/div[2]/ul/li[{i}]/div[1]/div/h4'
                element = driver.find_element(By.XPATH, xpath)
                texts = element.text
                
                Seal_name = texts.split('\n')[0]
                Seal_ratio = texts.split('| ')[-1]
                temp = pd.DataFrame({'직업' : [Job], 
                                     '직업각인' : [Seal], 
                                     '공통각인' : [Seal_name], 
                                     '공통각인 비중' : [Seal_ratio]
                                     })
                result_df = pd.concat([result_df, temp] , axis = 0)
                
            except : break
        

result_df['공통각인 비중'] = result_df['공통각인 비중'].apply(lambda x: float(x[:-1]))

#%%
result_df.to_csv('D:/github/lostark/241113_seal.csv', index = 0)

