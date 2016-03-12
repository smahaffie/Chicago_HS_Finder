'''Contains function to calculate user's tier
using existing CPS tool and selenium'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_tier_number(address):
    '''
	finds tier user falls in that is used to calculate 
	difficulty of admission to selective enrollment schools

	Inputs:
		address, string

	Returns:
		integer between 1 and 4
    '''
    driver = webdriver.Firefox()
    driver.get("http://cpstiers.opencityapps.org/")

    search_bar = driver.find_element_by_tag_name("Input")
    search_bar.send_keys(address)

    search_button = driver.find_element_by_id("btnSearch")
    search_button.click()

    tier_number_text = driver.find_element_by_id('tierNumber').text
    driver.close()

    return tier_number_text.split()[-1]
