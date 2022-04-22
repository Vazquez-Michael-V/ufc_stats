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
# WEBSITE = "https://www.ufc.com/athletes/all?filters%5B0%5D=status%3A23"
# driver.get(WEBSITE)
# driver.maximize_window()
# web_title = driver.title
# print(WEBSITE)
# print(web_title) 
# time.sleep(5)

def find_country_elements(driver):
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


def find_page_links(driver, df_temp):
    """Finds fighters' UFC webpages."""
    # Get the link to the figher's UFC webpage.
    fighter_page_link = driver.find_elements(By.CLASS_NAME, 'c-listing-athlete-flipcard__action')
    fighter_page_link_text = [link.find_element(By.TAG_NAME, 'a').get_attribute('href') for link in fighter_page_link]
    
    index_len = len(df_temp.index.values)
    if len(fighter_page_link_text) > index_len:
        fighter_page_link_text = ['Length of values error.']*index_len
        
    else:
        pass
    
    # ValueError occurs when #links on page > #names on page
    # df_temp['AthletePageLink'] = fighter_page_link_text  
    return fighter_page_link_text        

    
def find_record(driver, df_temp):
    """Finds fighters' records. Format (W-L-D)"""
    fighter_records = driver.find_elements(By.CLASS_NAME, 'c-listing-athlete__record')
    fighter_records_text = [record.text for record in fighter_records]

    index_len = len(df_temp.index.values)
    if len(fighter_records_text) > index_len:
        fighter_records_text = ['(W-L-D)']*index_len
        
    else:
        pass    
    
    return fighter_records_text

    
    