from django.shortcuts import render

from django.http import HttpResponse

from django import forms

import sqlite3

# Create your views here.

class FinderForm(forms.Form):
	your_address = forms.CharField(label='Your address', max_length = 100)
	distance = forms.CharField(label="Time you're willing to travel", max_length = 10, required=False)
	d_priority = forms.ChoiceField(label = "How important is the transit time?", choices = [(1,1),(2,2), (3,3), (4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)])
	schooltype = forms.MultipleChoiceField(label = "School type", required = False, widget=forms.CheckboxSelectMultiple(), choices = [(1,"Neighborhood"),(2,"Selective Enrollement"), (3,"Career Academy"), (4,"Magnet"),(5,"Contract"),(6,"Special Needs")])
	a_priority = forms.ChoiceField(label = "How important are academics?", choices = [(1,1),(2,2), (3,3), (4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)])
#temporary function
def get_travel_info_transit(address, address2):
	return 2000

def get_address(request):
	if request.method == "POST":
		form = FinderForm(request.POST) # request.GET
		if form.is_valid():
			# form.save()
			print(form.cleaned_data)

			connection = sqlite3.connect('CHSF.db')
			connection.create_function("time_between", 2, get_travel_info_transit)
			c = connection.cursor()

			time_between = """time_between("{}", address) < {}""".format(str(form.cleaned_data['your_address']),str(form.cleaned_data['distance']))

			query = "SELECT * FROM test WHERE " + time_between + ";"

			r = c.execute(query)
			results = r.fetchall()
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
