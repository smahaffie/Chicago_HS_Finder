from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import sqlite3

#Next line should come out eventually:
import googlemaps


class FinderForm(forms.Form):
    your_address = forms.CharField(label='Your address', max_length = 100)
    distance = forms.CharField(label="How many minutes are you willing to travel?", max_length = 10, required=False)
    d_priority = forms.ChoiceField(label = "How important is the transit time?", choices = [(1,1),(2,2), (3,3), (4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)])
    schooltype = forms.MultipleChoiceField(label = "School type", required = False, widget=forms.CheckboxSelectMultiple(), choices = [(1,"Neighborhood"),(2,"Selective Enrollement"), (3,"Career Academy"), (4,"Magnet"),(5,"Contract"),(6,"Special Needs")])
    
    a_priority = forms.ChoiceField(label = "How important are academics?", choices = [(1,1),(2,2), (3,3), (4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)])

'''
#temporary function
def get_travel_info_transit(address, address2):
    return 2000
'''


def get_address(request):
    if request.method == "POST":
        form = FinderForm(request.POST) # request.GET
        if form.is_valid():
            # form.save()
            print(form.cleaned_data)

            connection = sqlite3.connect('CHSF.db')
            connection.create_function("time_between", 2, get_duration)
            c = connection.cursor()

            time_between = "time_between('{}', address) < {}".format(str(form.cleaned_data['your_address']),str(form.cleaned_data['distance']))
            print(time_between)

            query = "SELECT name, address FROM addrs JOIN main ON addrs.school_id = main.school_id WHERE " + time_between + ";"
            print(query)

            r = c.execute(query)
            print('finished')
            results = r.fetchall()
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

    c = {'form': form}
    return render(request, 'matcher/start.html', c)



# THIS STUFF SHOULD NOT BE IN THIS FILE EVENTUALLY (see /Functions/google_maps.py):
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
