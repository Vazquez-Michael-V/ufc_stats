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
    
    return fighter_page_link_text        

    
def find_record(driver, df_temp):
    """Finds fighters' records. Format (W-L-D)"""
    fighter_records = driver.find_elements(By.CLASS_NAME, 'c-listing-athlete__record')
    fighter_records_text = [record.text for record in fighter_records]
    
    return fighter_records_text


# df_fighter_names = pd.read_excel('active_fighters_by_country.xlsx')
# print(df_fighter_names)

def delimit_record(df_fighter_names):
    """Takes the fighters DataFrame as arguement.\n
    (W-L-D) is split into 'Win', 'Loss', and 'Draw' columns.
    """
    df_fighter_names['FighterRecord'] = df_fighter_names['FighterRecord'].str.replace(' (W-L-D)', '', regex=False)
    df_fighter_names['Wins'] = df_fighter_names['FighterRecord']
    df_fighter_names[['Wins', 'Losses', 'Draws']] = df_fighter_names['Wins'].str.split('-', expand=True)
    
    numeric_cols = ['Wins', 'Losses', 'Draws']
    for col in numeric_cols:        
        df_fighter_names[col] = pd.to_numeric(df_fighter_names[col], errors='coerce').fillna(0).astype(int)    

    return df_fighter_names

# df_fighter_names = delimit_record(df_fighter_names)

# print(df_fighter_names)



