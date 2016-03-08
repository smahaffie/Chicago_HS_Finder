'''
Contains the specifications for the two forms that appear on the home page of the website
'''

from django import forms
from django.utils.safestring import mark_safe


class FinderForm2(forms.Form):
    '''
    Main user input forms
    '''
    reading_score = forms.IntegerField(label = 'NWEA Reading Percentile', 
        min_value = 0, max_value = 99)
    math_score = forms.IntegerField(label = 'NWEA Math Percentile',
     min_value = 0, max_value = 99)
    reading_grade = forms.ChoiceField(label = '7th Grade Reading Grade', 
        choices = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')])
    science_grade = forms.ChoiceField(label = '7th Grade Science Grade', 
        choices = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')])
    math_grade = forms.ChoiceField(label = '7th Grade Math Grade', 
        choices = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')])
    social_science_grade = forms.ChoiceField(label = '7th Grade Social Science Grade', 
        choices =[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')])

class FinderForm(forms.Form):
    '''
    Optional academic background form that only appears if user is interested in selective enrollment schools
    '''
    your_address = forms.CharField(label='Your address', max_length = 100)
    distance = forms.IntegerField(label="How many minutes are you willing to travel?", max_value = 10000, required = False, min_value = 1)
    d_priority = forms.ChoiceField(label = "How important is the transit time? (10 being most important)",  choices = [(1,1),(2,2), (3,3), (4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)])
    schooltype = forms.MultipleChoiceField(label = mark_safe("What types of schools are you interested in? (<a href='http://cps.edu/Schools/High_schools/Pages/Highschooltypes.aspx' target='_blank'> Read about your options here</a>)"),
        required = False, widget=forms.CheckboxSelectMultiple(), choices = 
        [('Neighborhood',"Neighborhood"),('Selective Enrollment',"Selective Enrollement"), ('Military Academy',"Military Academy"), 
        ('Magnet',"Magnet"),('Contract',"Contract"),('Special Needs',"Special Needs"),('Charter', 'Charter'),("International Baccalaureate", "International Baccalaureate")])
    
    a_priority = forms.ChoiceField(label = "How important are academics? (10 being most important)",  choices = [(1,1),(2,2), (3,3), (4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)])