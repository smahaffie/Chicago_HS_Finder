from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def abc(request):
    # return HttpResponse('Test')

    # c is context: way for you to put dynamic information through
    # your template

    c = {'name': 'Shelby', 
        'foods': ['sushi', 'dark chocolate']}

    return render(request, 'diary/start.html', c)
