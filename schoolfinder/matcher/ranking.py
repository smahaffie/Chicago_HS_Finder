import math
import json 

def rank_results(result_dict,form,tier=None,extra_form=None):
    point_ranges = []
    if extra_form != None:
        point_ranges = calc_difficulty(tier,extra_form)
    for school in result_dict:
        if school in point_ranges:
            result_dict[school]["difficulty"] = point_ranges[school]
        if form['distance']!=None:
            if extra_form != None:
                result_dict[school]["score"] = compute_score(school,form["d_priority"],form["a_priority"],result_dict[school], point_ranges,  form["distance"])
            else:
                result_dict[school]["score"] = compute_score(school,form["d_priority"],form["a_priority"],result_dict[school], form["distance"])
        else:
            if extra_form != None:
                result_dict[school]["score"] = compute_score(school,form["d_priority"],form["a_priority"],result_dict[school], point_ranges)
            else:
                result_dict[school]["score"] = compute_score(school,form["d_priority"],form["a_priority"],result_dict[school])
    sorting_dict = {}
    for school in result_dict:
        sorting_dict[result_dict[school]["score"]] = school

    sorted_school_ids = reversed(sorted(sorting_dict.keys()))

    final_list = []

    for score in sorted_school_ids:
        school_id = sorting_dict[score]
        data = []
        for key in ["website", "name","type", "time","ACT","enroll","persist","rating","score"]:
            point = result_dict[school_id][key]
            if point != None and point != '':
                data.append(point)
            else:
                if key != 'website':
                    data.append("Data not available")
                    print("appended not available!!!!")
                else:
                    # Not sure what to do in this case...
                    data.append(None)

        school_tup = tuple(data)
        final_list.append(school_tup)

    final_list = final_list[:12]

    return final_list

    



mult_dict = {1:0.1, 2:0.4, 3:0.6, 4:0.8, 5:1, 6:1.2, 7:1.4, 8:1.6, 9:1.8, 10:2.1}


def calc_difficulty(tier,extra_form):
    with open("../Clean Data/Data_Files/school_ranges.json",'r') as f:
        schoolranges = json.load(f)
    point_ranges = {}
    grade_values = {"A": 75, "B":50, "C": 25, "D": 0, "F":0 }
    test_scores = round(extra_form["reading_score"] * 1.515) + round(extra_form["math_score"] * 1.515)
    grade_pts = grade_values[extra_form["reading_grade"]] + grade_values[extra_form["math_grade"]] + grade_values[extra_form["science_grade"]] + grade_values[extra_form["social_science_grade"]]
    total_pts = test_scores + grade_pts
    for school in schoolranges:
        t = "Tier" + str(tier)
        max_ = int(schoolranges[school][t][1]) - total_pts
        min_ = int(schoolranges[school][t][0]) - total_pts
        point_ranges[school] = (min_,max_)

    return point_ranges

LAMBDA = 1/1000
def compute_score(school_id, d_pref, a_pref,  school_dict, point_ranges = None, max_willing=60):

    d_pref = mult_dict[int(d_pref)]
    a_pref = mult_dict[int(a_pref)]

    average_ACT = 18
    average_epct = 80
    average_ppct = 90

    print(school_dict['time'], max_willing)
    distance_score = 1 - (school_dict["time"]/max_willing) #distance to school / max distance willing to travel
    
    academic_factors = []
    
    if school_dict["ACT"] != None:
        school_act = (int(school_dict["ACT"])/average_ACT)
        academic_factors.append(school_act)
   
    if school_dict["enroll"] != None:
        school_enrollment_pct = (int(school_dict["enroll"])/average_epct)
        academic_factors.append(school_enrollment_pct)

    # take out second clause eventaully
    if school_dict["persist"] != None and school_dict['persist'] != '':
        school_persistance_pct = (int(school_dict["persist"])/average_ppct)
        academic_factors.append(school_persistance_pct)
   
    #if school["fot"] != None:
     #   school_on_track_rate = (on_track_rate/average_on_track_rate)
      #  academic_factors.append(school_on_track_rate)
    

    academic_score = sum(academic_factors)/len(academic_factors)

    prelim_score = d_pref * distance_score + a_pref * academic_score

    if point_ranges != None:
        if school_id in point_ranges:
            difficulty = (school_dict['difficulty'][0] + school_dict['difficulty'][1])/2

    

            #print(prelim_score, difficulty, LAMBDA)

            total_score = prelim_score - (LAMBDA * difficulty)

        else:
            total_score = prelim_score

    else:
        total_score = prelim_score

    return total_score
