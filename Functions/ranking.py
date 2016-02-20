import sqlite3
import math

mult_dict = {1:0.1, 2:0.4, 3:0.6, 4:0.8, 5:1, 6:1.2, 7:1.4, 8:1.6, 9:1.8, 10:2.1}

#INCLUDE PROPER DATABASE LOCATION BELOW
connection = sqlite3.connect('CHSF.db')
c = connection.cursor()


average = '''SELECT sum(total_tested*
composite_score_mean)/sum(total_tested) AS average
FROM act  WHERE year = 2015 AND category = "Overall" 
AND category_type = "Overall";'''

r = c.execute(average)
connection.close()

average_ACT = r.fetchall()

def get_multipliers(preferences):
    '''Given list of preferences where each preference is an integer,
    returns list of preference multipliers for use in ranking computation'''

    multipliers = []
    for preference in preferences:
        assert type(preference) = int and 1<=preference<=10
        multiplier = mult_dict[preference]
        multipliers.append(multiplier)
    return multipliers

def compute_ranking(preferences, user_inputs, distance_info, academic_info):
    '''Given list of preferences, distance_info tuple, and academic_info tuple,
    calculates ranking


    NOTE: preferences is list of integers inputted by user (scale 1:10)
    user_inputs is list of all user inputted values, first of which is max travel time
    distance_info is tuple where tuple[0] is distance to school
    academic_score is tuple where tuple[0] '''

    distance_score = 100 - 100(distance_info[0]/user_inputs[0]) #distance to school / max distance willing to travel
    academic_score = 