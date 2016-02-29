import sqlite3
import math

mult_dict = {1:0.1, 2:0.4, 3:0.6, 4:0.8, 5:1, 6:1.2, 7:1.4, 8:1.6, 9:1.8, 10:2.1}

#INCLUDE PROPER DATABASE LOCATION BELOW
connection = sqlite3.connect('../CHSF.db')
c = connection.cursor()


ACT_query = '''SELECT sum(total_tested*
composite_score_mean)/sum(total_tested) AS average
FROM act WHERE year = 2015 AND category = "Overall" 
AND category_type = "Overall";'''
print(ACT_query)
r = c.execute(ACT_query)

average_ACT = r.fetchall()
average_ACT = average_ACT[0][0]

EPCT_query = '''SELECT sum(graduates*
enrollment_pct)/sum(graduates) FROM cep;'''

r = c.execute(EPCT_query)
average_epct = r.fetchall()
average_epct = average_epct[0][0]

PPCT_query = '''SELECT sum(graduates*persist_pct)
/sum(graduates) FROM cep;'''

r = c.execute(PPCT_query)
average_ppct = r.fetchall()
average_ppct = average_ppct[0][0]

FOT_query = '''SELECT sum(num_fresh*fot)/
sum(num_fresh) FROM fot;'''

r = c.execute(FOT_query)
average_on_track_rate = r.fetchall()
average_on_track_rate = average_on_track_rate[0][0]



def calc_difficulty(tier,extra_form):
    with open("../Clean Data/Data_Files/school_ranges.json",'r') as f:
        schoolranges = json.load(f)
    point_ranges = {}
    grade_values = {"A": 75, "B":50, "C": 25, "D": 0, "F":0 }
    test_scores = round(extra_form["reading_score"] * 1.515) + round(extra_form["math_score"] * 1.515)
    grade_pts = grade_values[extra_form["reading_grade"]] + grade_values[extra_form["math_grade"]] + grade_values[extra_form["science_grade"]] + grade_values[inputs["social_science_grade"]]
    total_pts = test_scores + grade_pts
    for school in schoolranges:
        t = "Tier" + tier
        max_ = int(schoolranges[school][t][1]) - total_pts
        min_ = int(schoolranges[school][t][0]) - total_pts
        point_ranges[school] = (min_,max_)

    return point_ranges



def compute_score(school_id, d_pref, a_pref, max_willing, time_between, act_score, enrollment_pct, persistance_pct, on_track_rate=None):
    '''
    '''

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
