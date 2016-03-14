# We ran the code in this file only in order to create 
# a dictionary of all the schools in our database, 
# which we used with two Google Maps APIS:
# the directions API and the geolocation API.

import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def get_all():
    '''
    Returns a dictionary mapping the name of every school
    in the CPS system to its address
    '''

    addresses = {}

    driver = webdriver.Firefox()
    driver.get("http://schoolinfo.cps.edu/schoolprofile/SearchResults.aspx")

    std_notin = [0, 51, 52, 53, 54]

    get(driver.page_source, addresses, std_notin)

    for link in ['2','3','4','5','...', '7','8', '9', '10']:
        elements = driver.find_elements_by_tag_name("a")
        for element in elements:
            if element.text == link:
                element.click()
                break
        time.sleep(0.2)

        if link in ['2', '3', '4', '5']:
            get(driver.page_source, addresses, std_notin)
        if link in ['...', '7', '8', '9', '10']:
            get(driver.page_source, addresses, [50, 51])


    elements = driver.find_elements_by_tag_name("a")
    first = True
    for element in elements:
        if element.text == "...":
            if first:
                first = False
            else:
                element.click()
                break
    time.sleep(0.2)
    get(driver.page_source, addresses, std_notin)

    for link in ['12','13']:
        elements = driver.find_elements_by_tag_name("a")
        for element in elements:
            if element.text == link:
                element.click()
                break
        time.sleep(0.2)
        get(driver.page_source, addresses, std_notin)

    elements = driver.find_elements_by_tag_name("a")
    for element in elements:
            if element.text == '14':
                element.click()
                break
    time.sleep(0.2)
    get(driver.page_source, addresses, [0, 33, 34, 35, 36, 37])


    driver.close()

    return addresses

def get(html, addresses, notin):
    '''
    updates the addresses dictionary to include
    all the schools on one page. notin is a list of 
    all the tags that don't correspond to school
    table rows. 
    '''
    soup = bs4.BeautifulSoup(html, 'html5lib')

    results = []
    count = 0
    rows = soup.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        if len(tds) == 7:
            if count not in notin:
                results.append(tds)
            else:
                print(count)
            count += 1

    tmp = 0
    for result in results:
        school_name = result[1].find('a').text
        len_sn = len(school_name.split())
        address = " ".join(result[1].text.split()[len_sn:])
        addresses[school_name] = address
        tmp += 1
