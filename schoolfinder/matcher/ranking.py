''' contains all functions that process the data on schools returned by the 
SQL query to rank the schools and sort them based on their rankings '''
import math
import json 

def rank_results(result_dict,form,tier=None,extra_form=None):

    '''
    takes the schools returned by the SQL query and ranks them based on user preferences and data
    inputs:
        result_dict, SQL query results converted to a python dictionary
        form, cleaned data from django form
        tier, integer
        extra_form, cleaned data from second django form
    returns:
        final_list, python list, top 12 schools
    '''


    point_ranges = []
    if extra_form != None:
        point_ranges = calc_difficulty(tier,extra_form)
    for school in result_dict:
        if school in point_ranges:
            result_dict[school]["difficulty"] = point_ranges[school]
        if form['distance']!=None:
            if extra_form != None:
                result_dict[school]["score"] = compute_score(school,
                    form["d_priority"],form["a_priority"],result_dict[school],
                     point_ranges,  max_willing = form["distance"],tier=tier)
            else:
                result_dict[school]["score"] = compute_score(school,
                    form["d_priority"],form["a_priority"],result_dict[school], 
                    max_willing = form["distance"])
        else:
            if extra_form != None:
                result_dict[school]["score"] = compute_score(school,
                    form["d_priority"],form["a_priority"],result_dict[school], 
                    point_ranges,tier=tier)
            else:
                result_dict[school]["score"] = compute_score(school,
                    form["d_priority"],form["a_priority"],result_dict[school])
    sorting_dict = {}
    for school in result_dict:
        sorting_dict[result_dict[school]["score"]] = school

    sorted_school_ids = reversed(sorted(sorting_dict.keys()))

    final_list = []

    for score in sorted_school_ids:
        school_id = sorting_dict[score]
        data = []
        for key in ["website", "name","type", "time","ACT","enroll",
        "persist","rating","score","ptroutes", "FOT"]:
            point = result_dict[school_id][key]
            if point != None and point != '':
                data.append(point)
            else:
                if key != 'website':
                    data.append("Data not available")
                else:
                    data.append(None)

        school_tup = tuple(data)
        final_list.append(school_tup)

    final_list = final_list[:12] #only display top 12 schools

    return final_list




def calc_difficulty(tier,extra_form):
    '''
    calculates min and max points needed for admission to selective enrollment 
    schools based on student academics and historic data

    inputs:
        tier, string
        extra_form, cleaned django form data
    returns:
        point_ranges, python dictionary
    '''
    #file that contains min and max points needed for admission to selective
    #enrollment schools in 2015
    with open("../Clean Data/Data_Files/school_ranges.json",'r') as f:
        schoolranges = json.load(f)

    #we found the algorithm that CPS uses to assign point values to students
    #based on their academic background hardcoded into their website
    #the algorithm is used below to predict the score for users

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



def compute_score(school_id, d_pref, a_pref,  school_dict, point_ranges = None, max_willing=60, LAMBDA = 1/400,tier = None):
    '''
    ranks a school based on academics and distance to school_id
    Inputs:
        school_id, integer
        d_pref, integer
        a_pref, integer
        school_dict, python dictionary
        point_ranges, python dictionary
        max_willing, integer
    Returns:
        total_score, float

    '''
    #scales the preferences indicated by the user
    mult_dict = {1:0.1, 2:0.4, 3:0.6, 4:0.8, 5:1, 6:1.2, 7:1.4, 8:1.6,
     9:1.8, 10:2.1}

    d_pref = mult_dict[int(d_pref)]
    a_pref = mult_dict[int(a_pref)]

    #we used a SQL query (see the file gen_averages_table in Fuctions folder) 
    #to tabulate these values
    average_ACT = 18
    average_epct = 58.8
    average_ppct = 62.5
    average_fot = 84

    with open("../Clean Data/Data_Files/school_ranges.json",'r') as f:
        school_ranges = json.load(f)

    distance_score = 1 - (int(school_dict["time"])/max_willing) 
    
    academic_factors = []
    
    if school_dict["ACT"] != None:
        school_act = (int(school_dict["ACT"])/average_ACT)
        academic_factors.append(school_act)
   
    if school_dict["enroll"] != None:
        school_enrollment_pct = (int(school_dict["enroll"])/average_epct)
        academic_factors.append(school_enrollment_pct)

    if school_dict["persist"] != None and school_dict['persist'] != '':
        school_persistance_pct = (int(school_dict["persist"])/average_ppct)
        academic_factors.append(school_persistance_pct)

    
    if school_dict["FOT"] != None and school_dict["FOT"] != "":
        school_fot_pct = (int(school_dict["FOT"])/average_fot)
        academic_factors.append(school_fot_pct)

    academic_score = sum(academic_factors)/len(academic_factors)

    prelim_score = d_pref * distance_score + a_pref * academic_score
    print(school_ranges)
    if point_ranges != None: #factor in the difficult b/c its a selective school
        
        if school_id in point_ranges:
            difficulty = (school_dict['difficulty'][0] + school_dict['difficulty'][1])/2
            multiplier = point_ranges[school_id][0]/int(school_ranges[school_id]["Tier{}".format(tier)][0])
            total_score = prelim_score - (LAMBDA * multiplier * difficulty)

        else:
            total_score = prelim_score

    else: #not a selective school
        total_score = prelim_score

    return total_score
