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

def find_country_elements():
    """Returns a list of countries."""
    # UFC website 'Filters' button appears only after page has been clicked on.
    # Send 'Page Down' key to make the 'Filter' button appear.
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.send_keys(Keys.DOWN)
    
    filter_button = WebDriverWait(driver, 10).until(    
        EC.element_to_be_clickable((By.CLASS_NAME, 'e-button--small '))
        )
    
    filter_button.click()
    filters_country = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'facets-widget-ufc_facets_links'))
        ).find_elements(By.TAG_NAME, 'li')
    
    countries_text = [country.text for country in filters_country[1:]]

    return countries_text

    
countries_text = find_country_elements() 
print(countries_text)
print(len(countries_text))


df_fighter_names = pd.DataFrame()
for country in countries_text:
    print(f"Now clicking {country}.")
    country_button = driver.find_element(By.LINK_TEXT, country)
    country_button.click()
    time.sleep(5)
    
    fighter_names = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'l-flex--4col-1to4'))).find_elements(By.CLASS_NAME, 'c-listing-athlete__name')
    
    # Need a way to click the 'Load More Items' button.
    # view-items-wrp
    
    # Not all pages have a 'Load More' button.    
    while True:
        try:
            # load_more_button = WebDriverWait(driver, 5).until(
            #     EC.element_to_be_clickable((By.CLASS_NAME, 'js-pager__items pager'))
            #     )
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="block-mainpagecontent"]/div/div/div[2]/div/div/ul/li/a'))
                )           
        except TimeoutException:
            print("No 'Load More' button on page.")
            break
        else:
            print("Clicking 'Load More' button.")
            load_more_button.click()
            time.sleep(5)
        # Need a way to get the new fighters loaded on the page.
        # Might re-arrange the fighter_names and fighter_names_text lines.
        

    
    fighter_names_text = [name.text for name in fighter_names]
    print(fighter_names_text)
    df_temp = pd.DataFrame({'FighterNames' : fighter_names_text})
    
    df_temp['AthletePageLink'] = [driver.current_url]*len(list(df_temp['FighterNames']))
    df_temp['Country'] = [country]*len(list(df_temp['FighterNames']))
    
    
    df_temp.drop_duplicates(inplace = True)
    df_temp.reset_index(inplace = True, drop=True)
    df_fighter_names = df_fighter_names.append(df_temp)        

    print(df_temp)
    # print(df_fighter_names)    
    
    # Clicking back will remove the country filter from the website.
    driver.back()
    
    # Same code as when first landing on the webpage.
    # After driver.back(), webelements will be stale. Need to find elements again.    
    find_country_elements()   
   # find_country_elements() returns a list, but that should be fine here.
    
print("Done.")    

with pd.ExcelWriter('active_fighters_by_country.xlsx') as writer:
    df_fighter_names.to_excel(writer, sheet_name='FighterCountry')







