from django.shortcuts import render

from django.http import HttpResponse

from django import forms

import sqlite3

# Create your views here.

class FinderForm(forms.Form):
	your_address = forms.CharField(label='Your address', max_length = 100)
	distance = forms.CharField(label="Distance you're willing to travel", max_length = 10)

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

			query = """SELECT * FROM test WHERE time_between("{}",address) < "{}" """.format(
				str(form.cleaned_data['your_address']), str(form.cleaned_data['distance']))
			print(query)
			r = c.execute(query)
			results = r.fetchall()
			print("RESULTS:")
			print(results)
			print()
			context = {}
			context['names'] = []
			context['addresses'] = []
			for result in results:
				context['names'].append(result[0])
				context['addresses'].append(result[1])
			connection.close()
			print(context)

			return render(request, 'matcher/results.html', context)

	else:
		form = FinderForm()

	c = {'form': form}
	return render(request, 'matcher/start.html', c)

# def abc(request):
	# return render(request, 'matcher/start.html')