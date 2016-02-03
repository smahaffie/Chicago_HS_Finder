from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_neighborhood_schools(zipcode):
    '''
    Inputs: 
        zipcode: string or integer

    Returns:
        list of tuples of strings
    '''
    zipcode = str(zipcode)

    driver = webdriver.Firefox()
    driver.get("http://cps.edu/ScriptLibrary/Map-SchoolLocator2015/index.html")

    search_bar = driver.find_element_by_name("search")
    search_bar.clear()
    search_bar.send_keys(zipcode)
    search_bar.send_keys()

    search_button = driver.find_element_by_id("btnSearch")
    search_button.click()

    school_elements = driver.find_elements_by_class_name("resultsrow")
    schools = []
    for school_element in school_elements:
        schools.append(school_element.text.split())

    high_schools = []
    for school in schools:
        if school[-1][-1] == "*":
            if school[-1][-3:-1] == "12":
                high_schools.append(school)
        else:
            if school[-1][-2:] == "12":
                high_schools.append(school)

    driver.close()

    rv = []
    for high_school in high_schools:
        rv.append((" ".join(high_school[:-1]), high_school[-1]))

    return rv