import time
import random
import pandas as pd

# Import the library Selenium 
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

debug = False
city = 'vilnius'
save_to = './locations_' + city + '.csv'

# Make browser open in background 
options = webdriver.ChromeOptions() 
service = Service(executable_path = "C:/chromedriver-win64/chromedriver.exe")

# Create the webdriver object 
driver = webdriver.Chrome(service=service, options=options)

# Obtain the Google Map URL 
driver.get(f'https://www.google.com/maps/search/cafe+in+{city}/')
time.sleep(2)
#button = driver.find_element(By.XPATH, '//div[@data-is-touch-wrapper = "true"]')
elements = driver.find_elements(By.XPATH, '//div[@data-is-touch-wrapper = "true"]')

extracted = {}
extracted_names = []
extracted_address = []
extracted_latitudes = []
extracted_longitudes = []

def extract_lat_long(url: str):
    coords_start_index = url.find('@') + 1
    first_coma_index = url.find(',', coords_start_index)
    second_coma_index = url.find(',', first_coma_index + 1)
    
    return url[coords_start_index:first_coma_index], url[first_coma_index + 1:second_coma_index]


if debug:
    print(f"Total matching {len(elements)}")
    index = 0
    for el in elements:
        print(f"{index}: {el.text}")
        index += 1
button = elements[2]
button.click()

last_processed_index = 0
for page in range(10):
    entries_before = len(extracted)
    time.sleep(2)
    
    special_element = driver.find_element(By.XPATH, '//div[@role="feed" and @tabindex="-1"]')
    #scrollable_maybe = special_element.find_element(By.XPATH, './..') # parent

    driver.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight * 4);", special_element)
    time.sleep(2)
    
    map_elements = driver.find_elements(By.XPATH, '//a[@aria-label and @jsaction and not(@data-item-id)]')
    #print(f"Total map elements {len(map_elements)}")
    #print(map_elements)
    index = 0
    for el in map_elements:
        if index <= last_processed_index:
            index += 1
            continue
        try:
            info = el.get_attribute('aria-label')
        except StaleElementReferenceException:
            print(f"Passing map element at index {index}")
            index += 1
            continue
        print(f"{index}: {info}")
        if index > 0 and len(info) < 100:
            #el.click()
            driver.execute_script("arguments[0].click();", el)
            time.sleep(1 + random.randint(0,3))
            print(f"URL: {driver.current_url}")
            last_processed_index = index
            try:
                address_element = driver.find_element(By.XPATH, '//button[@data-item-id = "address"]')
                extracted[info] = address_element.get_attribute('aria-label')
                extracted_names.append(info)
                identifier_end_index = extracted[info].find(':')
                extracted_address.append(extracted[info][identifier_end_index + 2:])
                (lat, long) = extract_lat_long(driver.current_url)
                extracted_latitudes.append(lat)
                extracted_longitudes.append(long)
                
            except NoSuchElementException:
                print("Couldn't find address")
            try:
                close_button = driver.find_element(By.XPATH, '//button[@data-disable-idom = "true"]')
                close_button.click()
                time.sleep(1)
            except NoSuchElementException:
                print("Couldn't close")
                break
            
        index += 1
    entries_after = len(extracted)
    if entries_after == entries_before:
        #scrollable_area = driver.find_element(By.XPATH, '//div[@tabindex = "-1"]')
        #scrollable_area.send_keys(Keys.PAGE_DOWN)
    #else:
        break

time.sleep(10)

driver.quit()
print(extracted)

locations_dict = {'Name': extracted_names,
                  'Address': extracted_address,
                  'Latitude': extracted_latitudes,
                  'Longitude': extracted_longitudes}
df = pd.DataFrame(data=locations_dict)
df.to_csv(save_to)  


'''
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

service = Service(executable_path = "C:/chromedriver-win64/chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get('http://www.google.com/');
time.sleep(5) # Let the user actually see something!
button = driver.find_element(By.ID, 'W0wltc')
button.click()
time.sleep(4)
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()
'''