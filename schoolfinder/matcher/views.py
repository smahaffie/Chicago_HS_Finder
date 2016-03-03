from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import sqlite3
from django.utils.safestring import mark_safe
from .forms import FinderForm2, FinderForm
from .get_neighborhood_schools import get_neighborhood_schools, get_id_from_name, name_to_id
from .get_tier import get_tier_number
from .ranking import rank_results
# from .transit_info import get_duration, 


# import get_neighborhood_schools
#Next line should come out eventually:
import googlemaps
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json

def about(request):
    return render(request, 'matcher/about.html')


def build_query(neighborhood_schools, cleaned_data):
    '''
    Builds a SQL query based on user-inputs for schools to display in results
    Inputs:
        cleaned_data, Django form

    Returns:
        query, string
    '''
    
    neighborhood = False
    schooltypes = cleaned_data['schooltype']
    if 'Neighborhood' in schooltypes:
        schooltypes.remove('Neighborhood')
        neighborhood = True
    
    # If user checks no boxes, we will show them all school types. 
    if schooltypes == [] and neighborhood == False:
        neighborhood = True
        other_schooltypes = "('Selective Enrollment','Military Academy','Magnet','Contract','Special Needs','Charter')"

    elif len(schooltypes) == 1:
        other_schooltypes = "( '" + schooltypes[0] + "')"

    else:
        other_schooltypes = str(tuple(schooltypes))

    if cleaned_data["distance"] != None:
        seconds = int(cleaned_data["distance"]) * 60
        time_between = " AND ( time_between('{}', addrs.address) < {} )".format(str(cleaned_data['your_address'] + " Chicago, IL"),str(seconds))
    #else: #no max transit time specified
    #time_between = " "

    #print(time_between)

    neighborhood_q_string = ''
    if neighborhood:
        neighborhood_q_string = ' OR (school_type = "Neighborhood" AND school_id IN (SELECT main.school_id ' + \
            'FROM main JOIN addrs on addrs.school_id = main.school_id WHERE main.school_id in ' + str(neighborhood_schools) + ")) "

    # Remember to only calculate time between once, though!
    query = "SELECT main.name, main.school_id, main.school_type, act.composite_score_mean, main.rating, " + "time_between('{}', addrs.address) / 60, ".format(cleaned_data['your_address'] + " Chicago, IL") + "cep.enrollment_pct, cep.persist_pct FROM main LEFT OUTER JOIN act LEFT OUTER JOIN cep JOIN addrs " + \
                "ON main.school_id = act.school_id AND main.school_id = cep.school_id AND addrs.school_id = main.school_id" + \
                " WHERE act.category_type = 'Overall' AND act.year = '2015' AND (main.school_id in (SELECT school_id FROM main WHERE " + \
                ' (school_type IN ' + other_schooltypes + ")" + neighborhood_q_string + ")" + time_between + ");"                                    

    return query

def form(request):
    '''
    View that defines the starting page, the form where users provide Inputs
    Inputs:
        request, request object
    Returns:
        generate HTML page
    '''
    if request.method == "POST":
        form = FinderForm(request.POST) # request.GET
        extra_form = FinderForm2(request.POST)

        if form.is_valid():
            # form.save()
            print(form.cleaned_data)

            address = form.cleaned_data['your_address'] + " Chicago, IL"

            # if the user is interested in neighborhood schools, get a list of 
            # the neighborhood schools from the CPS schoolfinder tool.
            neighborhood_schools = []
            if 'Neighborhood' in form.cleaned_data['schooltype'] or form.cleaned_data['schooltype'] == []:
                neighborhood_schools = get_neighborhood_schools(address)

            if extra_form.is_valid():
                tier = int(get_tier_number(address))
                print("TIER NUMBER: {}".format(tier))

            # how to use this???

            connection = sqlite3.connect('CHSF.db')
            connection.create_function("time_between", 2, get_duration)
            c = connection.cursor()

            query = build_query(neighborhood_schools, form.cleaned_data)

            print(query)

            r = c.execute(query)
            results = r.fetchall()
            
            print('finished')
            print(results)
            context = {}
            context['names'] = []
            
            # ranking = rank_results(results,tier,form.cleaned_data,extra_form.cleaned_data) 

            for result in results:
                result_list= []
                for item in result:
                    result_list.append(item)
                context['names'].append(tuple(result_list))
            connection.close()

            return render(request, 'matcher/results.html', context)

    else:
        form = FinderForm()
        extra_form = FinderForm2()

    c = {'form': form, 'extra_form': extra_form}
    return render(request, 'matcher/start.html', c)

'''
def rank_results(results,tier,form,extra_form):
    result_dict = {}

    point_ranges = calc_difficulty(tier,extra_form)


    for result in results:
        s_id = result[1] #key is school id
        result_dict[s_id] = {} #dictionary to store query results 
        result_dict[s_id]["name"] = result[2]
        result_dict[s_id]["time"] = result[0]
        result_dict[s_id]["rating"] = result[5]
        result_dict[s_id]["ACT"] = result[4]
        result_dict[s_id]["type"] = result[3]
        if s_id in point_ranges:
            result_dict[s_id]["difficulty"] = point_ranges[s_id]
        result[s_id]["ranking"] = compute_score(s_id,form["d_priority"],form["a_priority"], form["distance"],result[0],result[4],result[6],result[7])

    print(result_dict)

import math

mult_dict = {1:0.1, 2:0.4, 3:0.6, 4:0.8, 5:1, 6:1.2, 7:1.4, 8:1.6, 9:1.8, 10:2.1}

#INCLUDE PROPER DATABASE LOCATION BELOW
def calculate_averages():
    #connection = sqlite3.connect('../CHSF.db')
    #c = connection.cursor()


    ACT_query = ''SELECT sum(total_tested*
    composite_score_mean)/sum(total_tested) AS average
    FROM act WHERE year = 2015 AND category = "Overall" 
    AND category_type = "Overall";''
    print(ACT_query)
    r = c.execute(ACT_query)

    average_ACT = r.fetchall()
    average_ACT = average_ACT[0][0]

    EPCT_query = ''SELECT sum(graduates*
    enrollment_pct)/sum(graduates) FROM cep;''

    r = c.execute(EPCT_query)
    average_epct = r.fetchall()
    average_epct = average_epct[0][0]

    PPCT_query = ''SELECT sum(graduates*persist_pct)
    /sum(graduates) FROM cep;''

    r = c.execute(PPCT_query)
    average_ppct = r.fetchall()
    average_ppct = average_ppct[0][0]

    FOT_query = ''SELECT sum(num_fresh*fot)/
    sum(num_fresh) FROM fot;''

    r = c.execute(FOT_query)
    average_on_track_rate = r.fetchall()
    average_on_track_rate = average_on_track_rate[0][0]
    #connection.close()


def calc_difficulty(tier,extra_form):
    with open("../Clean Data/Data_Files/school_ranges.json",'r') as f:
        schoolranges = json.load(f)
    point_ranges = {}
    grade_values = {"A": 75, "B":50, "C": 25, "D": 0, "F":0 }
    test_scores = round(extra_form["reading_score"] * 1.515) + round(extra_form["math_score"] * 1.515)
    grade_pts = grade_values[extra_form["reading_grade"]] + grade_values[extra_form["math_grade"]] + grade_values[extra_form["science_grade"]] + grade_values[extra_form["social_science_grade"]]
    total_pts = test_scores + grade_pts
    for school in schoolranges:
        t = "Tier" + str(tier)
        max_ = int(schoolranges[school][t][1]) - total_pts
        min_ = int(schoolranges[school][t][0]) - total_pts
        point_ranges[school] = (min_,max_)

    return point_ranges



def compute_score(school_id, d_pref, a_pref, max_willing, time_between, act_score, enrollment_pct, persistance_pct, on_track_rate=None):

    d_pref = mult_dict[d_pref]
    a_pref = mult_dict[a_pref]

    distance_score = 1 - (time_between/max_willing) #distance to school / max distance willing to travel
    
    academic_factors = []
    
    if act_score != None:
        school_act = (act_score/average_ACT)
        academic_factors.append(school_act)
    else:
        pass
    if enrollment_pct != None:
        school_enrollment_pct = (enrollment_pct/average_epct)
        academic_factors.append(school_enrollment_pct)
    else:
        pass
    if persistance_pct != None:
        school_persistance_pct = (persistance_pct/average_ppct)
        academic_factors.append(school_persistance_pct)
    else:
        pass
    if on_track_rate != None:
        school_on_track_rate = (on_track_rate/average_on_track_rate)
        academic_factors.append(school_on_track_rate)
    else:
        pass

    academic_score = sum(academic_factors)/len(academic_factors)

    prelim_score = d_pref * distance_score + a_pref * academic_score

    if school_id in schoolranges:
        difficulty = (point_ranges[school_id][0] + point_ranges[school_id][1])/2

    

        total_score = prelim_score - (LAMBDA * difficulty)

    else:
        total_score = prelim_score

    return total_score
'''

# FUNCTIONS THAT SHOULD BE IMPORTED IN EVENTUALLY:


'''
def get_id_from_name(schoolname):
    schoolname = schoolname.upper()
    if schoolname[-11:] != "High School":
        if schoolname[-2:] == "HS":
            schoolname = schoolname[:-2] + "HIGH SCHOOL"
        else:
            schoolname = schoolname + " HIGH SCHOOL"
    assert schoolname in name_to_id
    return name_to_id[schoolname]
'''









# NO 
def check_neighborhood_schools(school_id, neighborhood_schools):
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
    gmaps = googlemaps.Client(key='AIzaSyD12ij_d_fNk93dyugiVuJHSNvEagDNfSU')
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
    print("GET DURATION IN TRANSIT_INFO")
    print("Got duration")
    return get_travel_info_transit(str(home),str(school))[0]

