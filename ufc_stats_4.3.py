#Selenium imports for website navigation.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


#Pandas and numpy for data tables.
import pandas as pd
import numpy as np

import time

import json

import ufc_mods 

PATH = "C:\Program Files (x86)\chromedriver.exe" #Directory of the Chromedriver
serv = Service(PATH)
driver = webdriver.Chrome(service=serv)

# https://www.ufc.com/athletes/all
# Filtering to status = 'Active' redirects to this link: https://www.ufc.com/athletes/all?filters%5B0%5D=status%3A23
WEBSITE = "https://www.ufc.com/athletes/all?filters%5B0%5D=status%3A23"
driver.get(WEBSITE)
driver.maximize_window()
web_title = driver.title
print(WEBSITE)
print(web_title) 
time.sleep(5)



countries_text = ufc_mods.find_country_elements(driver) 
print(countries_text)
countries_total_num = len(countries_text)
print(f"{countries_total_num} countries found.")



df_fighter_names = pd.DataFrame()
countries_loaded = 0
for country in countries_text:
    print(f"Now clicking {country}.")
    country_button = driver.find_element(By.LINK_TEXT, country)
    country_button.click()
    time.sleep(5)

    # Look for the 'Load More' button.
    while True:
        try:
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="block-mainpagecontent"]/div/div/div[2]/div/div/ul/li/a'))
                )           
        except TimeoutException:
            print("No 'Load More' button on page.")   
            fighter_names = driver.find_elements(By.CLASS_NAME, 'c-listing-athlete__name')
            
            # Names are duplicated.
            fighter_names_text = [name.text for name in fighter_names]            
            country_list = [country]*len(fighter_names_text)
            
            print(len(fighter_names_text))
            df_temp = pd.DataFrame({'FighterName': fighter_names_text, 'Country': country_list})
            
            print(df_temp.shape)
            df_temp.drop_duplicates(subset=['FighterName'], inplace=True)
            
            # # Get the link to the figher's UFC webpage.
            # # ValueError occurs when #links on page > #names on page            
            fighter_page_link_text  = ufc_mods.find_page_links(driver, df_temp)
            df_temp['AthletePageLink'] = fighter_page_link_text          
            df_temp.reset_index(inplace=True, drop=True)
            
            fighter_records_text = ufc_mods.find_record(driver, df_temp)
            df_temp['FighterRecord'] = fighter_records_text
            print(fighter_records_text)
            
            df_fighter_names = df_fighter_names.append(df_temp)  
            print(df_fighter_names)
            # print(fighter_names_text)            
            
            countries_loaded+=1
            
            print(f"Done loading {country}.")   
            print(f"{countries_loaded}/{countries_total_num} of countries loaded.")
            time.sleep(5)
            driver.back()
            ufc_mods.find_country_elements(driver)             
            break
        
        else:
            print("Clicking 'Load More' button.")
            load_more_button.click()
            time.sleep(5)        

df_fighter_names.reset_index(inplace=True)
print(df_fighter_names)

with pd.ExcelWriter('active_fighters_by_country.xlsx') as writer:
    df_fighter_names.to_excel(writer, sheet_name='FighterCountry')


