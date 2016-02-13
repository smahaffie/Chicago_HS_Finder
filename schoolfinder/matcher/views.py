from django.shortcuts import render

from django.http import HttpResponse

from django import forms

# Create your views here.

class FinderForm(forms.Form):
	your_address = forms.CharField(label='Your address', max_length = 100)
	distance = forms.CharField(label="Distance you're willing to travel", max_length = 10)

def get_address(request):
	if request.method == "POST":
		form = FinderForm(request.POST) # request.GET
		if form.is_valid():
			# form.save()
			print(form.cleaned_data)
	else:
		form = FinderForm()

	c = {'form': form}
	return render(request, 'matcher/start.html', c)

# def abc(request):
	# return render(request, 'matcher/start.html')