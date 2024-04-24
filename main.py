from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import time
from bs4 import BeautifulSoup
import requests
import json

# Postavljanje encoding za standardni izlaz na UTF-8
sys.stdout.reconfigure(encoding='utf-8')

driver = webdriver.Firefox()

driver.get('https://www.kayak.com/flights/LAX-MLA/2024-05-24/2024-05-31?sort=bestflight_a')
time.sleep(5)

accept_all_xpath = "//button[@class='RxNS RxNS-mod-stretch RxNS-mod-variant-outline RxNS-mod-theme-base RxNS-mod-shape-default RxNS-mod-spacing-base RxNS-mod-size-small']"
folder = driver.find_element(By.XPATH, accept_all_xpath)

# Dobivanje teksta pronađenog elementa
folder_text = folder.text
print("Pronađeni element tekst:", folder_text)

# Kliknite na pronađeni element
folder.click()

flight_div_xpath = "//div[@class='nrc6-wrapper']"
flight_row = driver.find_elements(By.XPATH, flight_div_xpath)
#print(flight_row)


lista_letova = []
for WebElement in flight_row:
    elementHTML = WebElement.get_attribute('outerHTML')
    soup = BeautifulSoup(elementHTML, 'html.parser')

    #price
    temp_price = soup.find("div", {"class":"Oihj Oihj-mod-pres-default"})
    price = temp_price.find("div", {"class":"f8F1-price-text"})
    print(price.text)

    #kofer = temp_price.find("div", {"class":"ac27-inner"}
    #kofer
    kofer = temp_price.find_all("div", class_= "ac27-inner")
    print(kofer[1].text)

    #TODO Treba popraviti gresku  -- AttributeError -- ponekad se javlja prilikom uzimanja sadrzaja sa sajta
    # ? Mozda bi moglo da se napravi da se ponovo pokrene, jer kad ponovimo pozivanje posle greske ona nestane
    # Greska je javlja kad se pojavi jos jedan div mored onoga sto uzimamo
    
    new_dict = {
        "Price":price.text,
        "Koferi":kofer[1].text
    }
    print(new_dict)
    lista_letova.append(new_dict)


with open("Podaci.json", "w") as json_file:
    json.dump(lista_letova, json_file, indent=4)

print(lista_letova)



