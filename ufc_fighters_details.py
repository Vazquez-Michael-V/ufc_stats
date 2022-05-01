#Selenium imports for website navigation.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


#Pandas and numpy for data tables.
import pandas as pd
import numpy as np

import time

import json


PATH = "C:\Program Files (x86)\chromedriver.exe" #Directory of the Chromedriver
serv = Service(PATH)
driver = webdriver.Chrome(service=serv)


df_fighter_names = pd.read_excel('active_fighters_by_country.xlsx',
                                  usecols=['FighterName', 'Country', 'AthletePageLink']
                                 )

print(df_fighter_names.shape)
print(df_fighter_names.columns)
print(df_fighter_names)

# If Chrome crashes, change this to read the .pkl file.
# df_fighter_details = pd.read_pickle('df_fighter_details_err.pkl')

df_fighter_details = pd.DataFrame()

i = 0
for link in list(df_fighter_names['AthletePageLink']):
    fighter_dict = {}
    while True:
        try:
            driver.get(link)        
            # time.sleep(2)
            fighter_name = driver.title
            fighter_name = fighter_name.replace(' | UFC', '')
            print(fighter_name)
            # print(type(fighter_name))
            fighter_name_list = [fighter_name]
            fighter_dict['Name'] = fighter_name_list
            
            bio_label = driver.find_elements(By.CLASS_NAME, 'c-bio__label')
            
            bio_info = driver.find_elements(By.CLASS_NAME, 'c-bio__text')        
            
            bio_label_text = [label.text for label in bio_label]
            bio_info_text = [info.text for info in bio_info]
            # print(len(bio_label_text))
            # print(len(bio_info_text))
            
            bio_zip = zip(bio_label_text, bio_info_text)
            for a, b in bio_zip:      
                z = [b]
                fighter_dict[a] = z
                print(a, b)      
            
            print(fighter_dict)
            
            df_temp = pd.DataFrame(data=fighter_dict)
            print(df_temp)
            
            df_fighter_details = df_fighter_details.append(df_temp)
            
            # Don't lose current progress if Chrome crashes.
            df_fighter_details.to_pickle('df_fighter_details_err.pkl')            
            
            time.sleep(2)
            # driver.back()
            # time.sleep(2)
    
    
        except WebDriverException:
            # Don't lose current progress if Chrome crashes.
            df_fighter_details.to_pickle('df_fighter_details_err.pkl')
            
            print("Error occured, restarting browser.")
            driver.quit()
            PATH = "C:\Program Files (x86)\chromedriver.exe" #Directory of the Chromedriver
            serv = Service(PATH)
            driver = webdriver.Chrome(service=serv)
    
            # time.sleep(2)        
            # driver.get(link)        
            # time.sleep(2)        
        
        else:
            df_fighter_details.reset_index(inplace=True, drop=True)
            i +=1
            print(i)
            print(df_fighter_details)
            driver.quit()
            
            driver.quit()
            PATH = "C:\Program Files (x86)\chromedriver.exe" #Directory of the Chromedriver
            serv = Service(PATH)
            driver = webdriver.Chrome(service=serv)

            break
    

with pd.ExcelWriter('fighter_details.xlsx') as writer:
    df_fighter_details.to_excel(writer, sheet_name='details')











