'''
Contains all functions that use google maps to calculate transit-related
information between a given school and given home address

'''
import googlemaps
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def check_neighborhood_schools(school_id, neighborhood_schools):
    '''
    checks if a school is a neighborhood neighborhood_schools
    Inputs:
        school_id, integer
        neighborhood_schools, list of integers
    Returns:
        boolean
    '''
    if school_id in neighborhood_schools:
        return True

def find_best_route(home, school, travel_mode):
    '''
    Inputs:
        home: address string
        school: address string

    Returns:
        json
    '''
    gmaps = googlemaps.Client(key='AIzaSyCHtXoboDd-gh-swjytgWi_JkO1ObYJJYM')
    print("Starting gmaps")
    print(home, school, travel_mode)
    directions_json = gmaps.directions(home, school, mode=travel_mode)
    print("Got gmaps")
    best_route = directions_json[0]['legs'][0]
    return best_route


def get_travel_info_transit(home, school):
    '''
    Inputs:
        home: address string
        school: address string

    Returns:
        (trip duration in seconds, 
        time spent walking in seconds, 
        list of tuples of form (type, line/route name) for each public transportation route taken)
    '''
    print("GET TRAVEL INFO IN TRANSIT_INFO")
    best_route = find_best_route(home, school, 'transit')

    duration_text = best_route['duration']['text']
    duration = best_route['duration']['value']

    walking_time = 0 # in seconds
    ptroutes = []
    for step in best_route['steps']:
        if step['travel_mode'] == "WALKING":
            walking_time += step['duration']['value']
        elif step['travel_mode'] == 'TRANSIT':
            if 'line' in step['transit_details']:
                line = step['transit_details']['line']
                if 'short_name' in line['vehicle']['type']:
                    ptroutes.append((line['vehicle']['type'], line['short_name']))
                elif 'name' in line:
                    ptroutes.append((line['vehicle']['type'], line['name']))

    return [duration, walking_time, ptroutes]

def get_duration(home, school):
    '''
    parses results of get_travel_info_transit to return total transit walking_time

    Inputs:
        home, string
        school, string

    Returns:
        transit time, integer
    '''
    print("GET DURATION IN TRANSIT_INFO")
    print("Got duration")
    return get_travel_info_transit(str(home),str(school))[0]

def get_ptroutes(home, school):
    walking_time = int(round(get_travel_info_transit(str(home),str(school))[1] / 60))
    return walking_time