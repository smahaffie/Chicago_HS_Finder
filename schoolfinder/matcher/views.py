from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import sqlite3

# import get_neighborhood_schools
#Next line should come out eventually:
import googlemaps
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class FinderForm2(forms.Form):
    your_score = forms.CharField(label = 'Your score', max_length = 100)

class FinderForm(forms.Form):
    your_address = forms.CharField(label='Your address', max_length = 100)
    distance = forms.CharField(label="How many minutes are you willing to travel?", max_length = 10, required=False)
    d_priority = forms.ChoiceField(label = "How important is the transit time?", choices = [(1,1),(2,2), (3,3), (4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)])
    schooltype = forms.MultipleChoiceField(label = "School type", 
        required = False, widget=forms.CheckboxSelectMultiple(), choices = 
        [('Neighborhood',"Neighborhood"),('Selective Enrollment',"Selective Enrollement"), ('Career Academy',"Career Academy"), 
        ('Magnet',"Magnet"),('Contract',"Contract"),('Special Needs',"Special Needs")])
    
    a_priority = forms.ChoiceField(label = "How important are academics?", choices = [(1,1),(2,2), (3,3), (4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)])

def get_address(request):
    if request.method == "POST":
        form = FinderForm(request.POST) # request.GET
        extra_form = FinderForm2(request.POST)

        if form.is_valid():
            # form.save()
            print(form.cleaned_data)

            neighborhood_schools = get_neighborhood_schools(form.cleaned_data['your_address'])
            print(type(neighborhood_schools))
            print(neighborhood_schools)
            print(str(neighborhood_schools))

            # how to use this???

            connection = sqlite3.connect('CHSF.db')
            connection.create_function("time_between", 2, get_duration)
            c = connection.cursor()

            print(form.cleaned_data)

            time_between = "time_between('{}', addrs.address) < {}".format(str(form.cleaned_data['your_address']),str(form.cleaned_data['distance']))

            query = "SELECT main.school_id, main.name, main.school_type, act.composite_score_mean, fot.fot, main.rating FROM main JOIN fot JOIN act JOIN cep JOIN addrs " + \
                "ON main.school_id = fot.school_id AND main.school_id = act.school_id AND main.school_id = cep.school_id AND addrs.school_id = main.school_id" + \
                " WHERE act.category_type = 'Overall' AND act.year = '2015' AND main.school_id in (SELECT school_id FROM main WHERE " + \
                ' (school_type IN ("Selective Enrollment","Magnet","Contract","Options","Reinvestment", "Charter") OR (school_type = "Neighborhood" AND school_id IN ' + \
                '(SELECT main.school_id FROM main JOIN addrs on addrs.school_id = main.school_id WHERE main.school_id in ' + str(neighborhood_schools) + ")" + ") " + \
                "AND " + time_between + "));"


            print(query)

            r = c.execute(query)
            results = r.fetchall()
            print('finished')
            print(results)
            context = {}
            context['names'] = []
            context['addresses'] = []
            for result in results:
                context['names'].append((result[0],result[1]))
            connection.close()

            return render(request, 'matcher/results.html', context)

    else:
        form = FinderForm()
        extra_form = FinderForm2()

    c = {'form': form}
    return render(request, 'matcher/start.html', c)



# FUNCTIONS THAT SHOULD BE IMPORTED IN EVENTUALLY:
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
    print("Got duration")
    return get_travel_info_transit(str(home),str(school))[0]

def get_neighborhood_schools(address):
    '''
    Inputs: 
        address: string

    Returns:
        list of school ids
    '''

    driver = webdriver.Firefox()
    driver.get("http://cps.edu/ScriptLibrary/Map-SchoolLocator2015/index.html")

    search_bar = driver.find_element_by_name("search")
    search_bar.clear()
    search_bar.send_keys(address)
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

    rvl = []
    for high_school in high_schools:
        rvl.append(str(get_id_from_name(" ".join(high_school[:-1]))))

    print(rvl)

    if len(rvl) == 1:
        rv = "(" + str(rvl[0]) + ")" 

    else:
        rv = str(tuple(rvl))

    return rv

def get_id_from_name(schoolname):
    schoolname = schoolname.upper()
    if schoolname[-11:] != "High School":
        if schoolname[-2:] == "HS":
            schoolname = schoolname[:-2] + "HIGH SCHOOL"
        else:
            schoolname = schoolname + " HIGH SCHOOL"
    assert schoolname in name_to_id
    return name_to_id[schoolname]

name_to_id = {'ACE TECH HIGH SCHOOL': '400010',
 'AIR FORCE HIGH SCHOOL': '610513',
 'ALCOTT HIGH SCHOOL': '610524',
 'AMANDLA HIGH SCHOOL': '400012',
 'AMUNDSEN HIGH SCHOOL': '609695',
 'ASPIRA - EARLY COLLEGE HIGH SCHOOL': '400013',
 'AUSTIN BUS & ENTRP HIGH SCHOOL': '400018',
 'AUSTIN POLY HIGH SCHOOL': '610501',
 'BACK OF THE YARDS HIGH SCHOOL': '610563',
 'BANNER WEST HIGH SCHOOL': '610555',
 'BOGAN HIGH SCHOOL': '609698',
 'BOWEN HIGH SCHOOL': '610323',
 'BRONZEVILLE HIGH SCHOOL': '610381',
 'BROOKS HIGH SCHOOL': '609726',
 'CAMELOT - CHICAGO EXCEL HIGH SCHOOL': '400147',
 'CAMELOT - EXCEL ENGLEWOOD HIGH SCHOOL': '610565',
 'CAMELOT - EXCEL SOUTHWEST HIGH SCHOOL': '400176',
 'CAMELOT - EXCEL WOODLAWN HIGH SCHOOL': '400175',
 'CAMELOT SAFE HIGH SCHOOL': '610573',
 'CARVER MILITARY HIGH SCHOOL': '609760',
 'CATALYST - MARIA HIGH SCHOOL': '400115',
 'CHICAGO ACADEMY HIGH SCHOOL': '610340',
 'CHICAGO AGRICULTURE HIGH SCHOOL': '609753',
 'CHICAGO ARTS HIGH SCHOOL': '400022',
 'CHICAGO MATH & SCIENCE HIGH SCHOOL': '400035',
 'CHICAGO MILITARY HIGH SCHOOL': '609754',
 'CHICAGO TECH HIGH SCHOOL': '400091',
 'CHICAGO VIRTUAL HIGH SCHOOL': '400036',
 'CHICAGO VOCATIONAL HIGH SCHOOL': '609674',
 'CICS - CHICAGOQUEST HIGH SCHOOL': '400113',
 'CICS - ELLISON HIGH SCHOOL': '400032',
 'CICS - HAWKINS HIGH SCHOOL': '400108',
 'CICS - LONGWOOD HIGH SCHOOL': '400033',
 'CICS - NORTHTOWN HIGH SCHOOL': '400034',
 'CLARK HIGH SCHOOL': '610244',
 'CLEMENTE HIGH SCHOOL': '609759',
 'COLLINS HIGH SCHOOL': '610499',
 'COMMUNITY SERVICES WEST HIGH SCHOOL': '400038',
 'CORLISS HIGH SCHOOL': '609761',
 'CRANE MEDICAL HIGH SCHOOL': '610561',
 'CURIE HIGH SCHOOL': '609756',
 'DEVRY HIGH SCHOOL': '610402',
 'DISNEY II HIGH SCHOOL': '610564',
 'DOUGLASS HIGH SCHOOL': '610245',
 'DUNBAR HIGH SCHOOL': '609676',
 'EPIC HIGH SCHOOL': '400094',
 'FARRAGUT HIGH SCHOOL': '609704',
 'FENGER HIGH SCHOOL': '609705',
 'FOREMAN HIGH SCHOOL': '609708',
 'GAGE PARK HIGH SCHOOL': '609709',
 'GOODE HIGH SCHOOL': '610558',
 'GRAHAM HIGH SCHOOL': '609769',
 'HANCOCK HIGH SCHOOL': '609694',
 'HARLAN HIGH SCHOOL': '609710',
 'HARPER HIGH SCHOOL': '609711',
 'HIRSCH HIGH SCHOOL': '609712',
 'HOPE HIGH SCHOOL': '609768',
 'HUBBARD HIGH SCHOOL': '609741',
 'HYDE PARK HIGH SCHOOL': '609713',
 'INFINITY HIGH SCHOOL': '610384',
 'INSTITUTO - HEALTH HIGH SCHOOL': '400104',
 'INSTITUTO - LOZANO HIGH SCHOOL': '400148',
 'INSTITUTO - LOZANO MASTERY HIGH SCHOOL': '400164',
 'INTRINSIC HIGH SCHOOL': '400162',
 'JEFFERSON HIGH SCHOOL': '609783',
 'JONES HIGH SCHOOL': '609678',
 'JUAREZ HIGH SCHOOL': '609764',
 'JULIAN HIGH SCHOOL': '609762',
 'KELLY HIGH SCHOOL': '609715',
 'KELVYN PARK HIGH SCHOOL': '609716',
 'KENNEDY HIGH SCHOOL': '609718',
 'KENWOOD HIGH SCHOOL': '609746',
 'KING HIGH SCHOOL': '609751',
 'LAKE VIEW HIGH SCHOOL': '609719',
 'LANE TECH HIGH SCHOOL': '609720',
 'LEGAL PREP HIGH SCHOOL': '400119',
 'LINCOLN PARK HIGH SCHOOL': '609738',
 'LINDBLOM HIGH SCHOOL': '610391',
 'LITTLE BLACK PEARL HIGH SCHOOL': '400137',
 'MAGIC JOHNSON - ENGLEWOOD HIGH SCHOOL': '610582',
 'MAGIC JOHNSON - HUMBOLDT PK HIGH SCHOOL': '610580',
 'MAGIC JOHNSON - N LAWNDALE HIGH SCHOOL': '610566',
 'MAGIC JOHNSON - ROSELAND HIGH SCHOOL': '610567',
 'MANLEY HIGH SCHOOL': '609722',
 'MARINE LEADERSHIP AT AMES HIGH SCHOOL': '609780',
 'MARINE MILITARY HIGH SCHOOL': '610502',
 'MARSHALL HIGH SCHOOL': '609723',
 'MATHER HIGH SCHOOL': '609724',
 'MORGAN PARK HIGH SCHOOL': '609725',
 'MULTICULTURAL HIGH SCHOOL': '610385',
 'NOBLE - ACADEMY HIGH SCHOOL': '400170',
 'NOBLE - BAKER HIGH SCHOOL': '400157',
 'NOBLE - BULLS HIGH SCHOOL': '400097',
 'NOBLE - BUTLER HIGH SCHOOL': '400156',
 'NOBLE - COMER HIGH SCHOOL': '400052',
 'NOBLE - DRW HIGH SCHOOL': '400118',
 'NOBLE - GOLDER HIGH SCHOOL': '400053',
 'NOBLE - HANSBERRY HIGH SCHOOL': '400117',
 'NOBLE - ITW SPEER HIGH SCHOOL': '400169',
 'NOBLE - JOHNSON HIGH SCHOOL': '400106',
 'NOBLE - MUCHIN HIGH SCHOOL': '400098',
 'NOBLE - NOBLE HIGH SCHOOL': '400051',
 'NOBLE - PRITZKER HIGH SCHOOL': '400054',
 'NOBLE - RAUNER HIGH SCHOOL': '400055',
 'NOBLE - ROWE CLARK HIGH SCHOOL': '400056',
 'NOBLE - UIC HIGH SCHOOL': '400057',
 'NORTH LAWNDALE - CHRISTIANA HIGH SCHOOL': '400058',
 'NORTH LAWNDALE - COLLINS HIGH SCHOOL': '400059',
 'NORTH-GRAND HIGH SCHOOL': '609691',
 'NORTHSIDE LEARNING HIGH SCHOOL': '609744',
 'NORTHSIDE PREP HIGH SCHOOL': '609749',
 'OGDEN HIGH SCHOOL': '610529',
 'OMBUDSMAN - NORTHWEST HIGH SCHOOL': '610569',
 'OMBUDSMAN - SOUTH HIGH SCHOOL': '610570',
 'OMBUDSMAN - WEST HIGH SCHOOL': '610571',
 'ORR HIGH SCHOOL': '610389',
 'PATHWAYS - ASHBURN HIGH SCHOOL': '610557',
 'PATHWAYS - AVONDALE HIGH SCHOOL': '610568',
 'PATHWAYS - BRIGHTON PARK HIGH SCHOOL': '400173',
 'PAYTON HIGH SCHOOL': '609680',
 'PEACE AND EDUCATION HIGH SCHOOL': '610386',
 'PERSPECTIVES - JOSLIN HIGH SCHOOL': '400064',
 'PERSPECTIVES - LEADERSHIP HIGH SCHOOL': '400061',
 'PERSPECTIVES - MATH & SCI HIGH SCHOOL': '400066',
 'PERSPECTIVES - TECH HIGH SCHOOL': '400062',
 'PHILLIPS HIGH SCHOOL': '609727',
 'PHOENIX MILITARY HIGH SCHOOL': '610304',
 'PROLOGUE - EARLY COLLEGE HIGH SCHOOL': '400070',
 'PROLOGUE - JOHNSTON HIGH SCHOOL': '400109',
 'PROLOGUE - WINNIE MANDELA HIGH SCHOOL': '610574',
 'PROSSER HIGH SCHOOL': '609679',
 'RABY HIGH SCHOOL': '610334',
 'RICHARDS HIGH SCHOOL': '609682',
 'RICKOVER MILITARY HIGH SCHOOL': '610390',
 'ROBESON HIGH SCHOOL': '609707',
 'ROOSEVELT HIGH SCHOOL': '609728',
 'SCHURZ HIGH SCHOOL': '609729',
 'SENN HIGH SCHOOL': '609730',
 'SHABAZZ - DUSABLE HIGH SCHOOL': '400073',
 'SIMEON HIGH SCHOOL': '609692',
 'SIMPSON HIGH SCHOOL': '609750',
 'SOCIAL JUSTICE HIGH SCHOOL': '610383',
 'SOLORIO HIGH SCHOOL': '610543',
 'SOUTH SHORE INTL HIGH SCHOOL': '610547',
 'SOUTHSIDE HIGH SCHOOL': '609745',
 'SPRY HIGH SCHOOL': '610357',
 'STEINMETZ HIGH SCHOOL': '609732',
 'SULLIVAN HIGH SCHOOL': '609733',
 'TAFT HIGH SCHOOL': '609734',
 'TEAM HIGH SCHOOL': '610506',
 'TILDEN HIGH SCHOOL': '609735',
 'U OF C - WOODLAWN HIGH SCHOOL': '400077',
 'UNO - GARCIA HIGH SCHOOL': '400085',
 'UNO - ROGERS PARK HIGH SCHOOL': '400121',
 'UNO - SOCCER HIGH SCHOOL': '400149',
 'UPLIFT HIGH SCHOOL': '610394',
 'URBAN PREP - BRONZEVILLE HIGH SCHOOL': '400105',
 'URBAN PREP - ENGLEWOOD HIGH SCHOOL': '400086',
 'URBAN PREP - WEST HIGH SCHOOL': '400102',
 'VAUGHN HIGH SCHOOL': '609766',
 'VOISE HIGH SCHOOL': '610518',
 'VON STEUBEN HIGH SCHOOL': '609737',
 'WASHINGTON HIGH SCHOOL': '609739',
 'WELLS HIGH SCHOOL': '609740',
 'WESTINGHOUSE HIGH SCHOOL': '609693',
 'WILLIAMS HIGH SCHOOL': '610380',
 'WORLD LANGUAGE HIGH SCHOOL': '610392',
 'YCCS - ADDAMS HIGH SCHOOL': '400134',
 'YCCS - ASPIRA PANTOJA HIGH SCHOOL': '400125',
 'YCCS - ASSOCIATION HOUSE HIGH SCHOOL': '400126',
 'YCCS - AUSTIN CAREER HIGH SCHOOL': '400127',
 'YCCS - CAMPOS HIGH SCHOOL': '400131',
 'YCCS - CCA ACADEMY HIGH SCHOOL': '400128',
 'YCCS - CHATHAM HIGH SCHOOL': '400150',
 'YCCS - HOUSTON HIGH SCHOOL': '400129',
 'YCCS - INNOVATIONS HIGH SCHOOL': '400133',
 'YCCS - LATINO YOUTH HIGH SCHOOL': '400135',
 'YCCS - MCKINLEY HIGH SCHOOL': '400124',
 'YCCS - OLIVE HARVEY HIGH SCHOOL': '400136',
 'YCCS - SCHOLASTIC ACHIEVEMENT HIGH SCHOOL': '400123',
 'YCCS - SULLIVAN HIGH SCHOOL': '400139',
 'YCCS - TRUMAN HIGH SCHOOL': '400141',
 'YCCS - VIRTUAL HIGH SCHOOL': '400142',
 'YCCS - WEST TOWN HIGH SCHOOL': '400143',
 'YCCS - WESTSIDE HOLISTIC HIGH SCHOOL': '400144',
 'YCCS - YOUTH CONNECTION HIGH SCHOOL': '400145',
 'YCCS - YOUTH DEVELOPMENT HIGH SCHOOL': '400130',
 'YORK HIGH SCHOOL': '609748',
 'YOUNG HIGH SCHOOL': '609755',
 'YOUNG WOMENS HIGH SCHOOL': '400087'}
