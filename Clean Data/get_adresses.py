import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def get_all():
    '''Aggregate function of get, get2, and get3, 
    which allows us to get all addresses for schools on our list
    of plausible schools'''
    addresses = {}

    driver = webdriver.Firefox()
    driver.get("http://schoolinfo.cps.edu/schoolprofile/SearchResults.aspx")

    get(driver.page_source, addresses)

    for link in ['2','3','4','5']:
        elements = driver.find_elements_by_tag_name("a")
        for element in elements:
            if element.text == link:
                element.click()
                break

        a = driver.page_source
        get(driver.page_source, addresses)

    for link in ['...', '7','8', '9', '10']:
        elements = driver.find_elements_by_tag_name("a")
        for element in elements:
            if element.text == link:
                element.click()
                break

        a = driver.page_source
        time.sleep(0.2)
        get2(driver.page_source, addresses)


    elements = driver.find_elements_by_tag_name("a")
    first = True
    for element in elements:
        if element.text == "...":
            if first:
                first = False
            else:
                element.click()
                break

    a = driver.page_source
    time.sleep(0.2)
    get(driver.page_source, addresses)

    for link in ['12','13']:
        elements = driver.find_elements_by_tag_name("a")
        for element in elements:
            if element.text == link:
                element.click()
                break

        a = driver.page_source
        time.sleep(0.2)
        get(driver.page_source, addresses)

    elements = driver.find_elements_by_tag_name("a")
    for element in elements:
            if element.text == '14':
                element.click()
                break

    a = driver.page_source
    time.sleep(0.2)
    get3(driver.page_source, addresses)


    driver.close()

    return addresses

def get(html, addresses):
    '''

    '''

    print("BEFORE ", len(addresses))
    soup = bs4.BeautifulSoup(html, 'html5lib')

    results = []
    count = 0
    rows = soup.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        if len(tds) == 7:
            if count not in [0, 51, 52, 53, 54]:
                results.append(tds)
            else:
                print(count)
            count += 1

    tmp = 0
    for result in results:
        try:
            school_name = result[1].find('a').text
        except:
            print("error=",result, len(results))

        len_sn = len(school_name.split())
        address = " ".join(result[1].text.split()[len_sn:])
        addresses[school_name] = address
        print(tmp, school_name)
        tmp += 1

    print("AFTER ", len(addresses))
  



def get2(html, addresses):
    print("BEFORE", len(addresses))
    soup = bs4.BeautifulSoup(html, 'html5lib')

    results = []
    count = 0
    rows = soup.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        if len(tds) == 7:
            if count not in [50, 51]:
                results.append(tds)
            else:
                print(count)
            count += 1

    tmp = 0
    for result in results:
        try:
            school_name = result[1].find('a').text
        except:
            print("error=",result, len(results))

        len_sn = len(school_name.split())
        address = " ".join(result[1].text.split()[len_sn:])
        addresses[school_name] = address
        print(tmp, school_name)
        tmp += 1

    print("AFTER", len(addresses))

def get3(html, addresses):
    print("BEFORE ", len(addresses))
    soup = bs4.BeautifulSoup(html, 'html5lib')

    results = []
    count = 0
    rows = soup.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        if len(tds) == 7:
            if count not in [0, 33, 34, 35, 36, 37]:
                results.append(tds)
            else:
                print(count)
            count += 1

    tmp = 0
    for result in results:
        try:
            school_name = result[1].find('a').text
        except:
            print("error=",result, len(results))

        len_sn = len(school_name.split())
        address = " ".join(result[1].text.split()[len_sn:])
        addresses[school_name] = address
        print(tmp, school_name)
        tmp += 1

    print("AFTER ", len(addresses))
