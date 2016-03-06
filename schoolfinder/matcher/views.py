from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import sqlite3
from django.utils.safestring import mark_safe
from .forms import FinderForm2, FinderForm
from .get_neighborhood_schools import get_neighborhood_schools, get_id_from_name, name_to_id
from .get_tier import get_tier_number
from .ranking import rank_results
from .transit_info import *
import googlemaps
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
from .build_query import build_query

def about(request):
    return render(request, 'matcher/about.html')


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

            tier = None
            if extra_form.is_valid():
                tier = int(get_tier_number(address))
                print("TIER NUMBER: {}".format(tier))

            # how to use this???

            connection = sqlite3.connect('CHSF.db')
            connection.create_function("time_between", 2, get_duration)
            connection.create_function("ptroutes", 2, get_ptroutes)
            c = connection.cursor()

            query = build_query(neighborhood_schools, form.cleaned_data)

            print(query)

            r = c.execute(query)
            results = r.fetchall()
            
            print('finished')
            print(results)
            context = {}
            context['names'] = []
            context['map_info'] = []

            # ranking = rank_results(results,tier,form.cleaned_data,extra_form.cleaned_data) 
            zIndex = 1
            result_dict = {}
            for result in results:
                s_id = result[2] #key is school id
                result_dict[s_id] = {} #dictionary to store query results 
                result_dict[s_id]["name"] = result[1]
                result_dict[s_id]["address"] = result[0]
                result_dict[s_id]["rating"] = result[5]
                result_dict[s_id]["ACT"] = result[4]
                result_dict[s_id]["type"] = result[3]
                result_dict[s_id]["website"] = result[6]
                result_dict[s_id]["time"] = result[7]
                result_dict[s_id]["enroll"] = result[8]
                result_dict[s_id]["persist"] = result[9]
                result_dict[s_id]['ptroutes'] = result[10]
                lat, lng = get_geolocation(result_dict[s_id]['address'])
                context['map_info'].append([result_dict[s_id]['name'], lat, lng, zIndex])
                zIndex += 1

            print(tier)
            if tier != None:
                print("CASE 1")
                rank_dict = rank_results(result_dict,form.cleaned_data,tier,extra_form.cleaned_data)
            else:
                print('CASE 2')
                rank_dict = rank_results(result_dict,form.cleaned_data)
                
            context["names"] = rank_dict





            connection.close()

            print("CONTEXT")
            print(context['map_info'])

            return render(request, 'matcher/results.html', context)

    else:
        form = FinderForm()
        extra_form = FinderForm2()

    c = {'form': form, 'extra_form': extra_form}
    return render(request, 'matcher/start.html', c)

def get_geolocation(address):
    gmapsgeo = googlemaps.Client(key='AIzaSyD12ij_d_fNk93dyugiVuJHSNvEagDNfSU')
    result = gmapsgeo.geocode(address)[0]['geometry']['location']

    return result['lat'], result['lng']

