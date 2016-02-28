'''function that takes NWEA Reading Percentile, NWEA Math Percentile, 
7th Grade Reading Grade, 7th Grade Math Grade,7th Grade Science Grade,
7th Grade Social Studies Grade, and tier and returns score range '''

import csv

#inputs just for testing
inputs = {"readingTest": 90, "mathTest": 90, "readingGrade": "A", "mathGrade": "B", "scienceGrade": "B", "socialGrade": "C", "tier": 1}
grade_values = {"A": 75, "B":50, "C": 25, "D": 0, "F":0 }
csv = '../Clean Data/Data_Files/Cutoff_Scores_2015_2016'


name_id_dict = {'King':609751, 'Brooks':609726, 'Hancock':609694, 'Jones': 609678, 'Lane':609720, 'Lindblom': 610391,
'Northside':609749, 'Payton':609680, 'South Shore':610547, 'Westinghouse':609693, 'Young':609755}


def create_min_max_dict(csv):
    '''
    Creates a python dictionary from csv file that lists poitns needed for each school by tier
    '''
    school_ranges = {}
    with open(csv,'r') as f:
        f.readline()
        for row in f:
            print(row)
            fields = row.strip().split(",")
            key = "{}{}".format(fields[1],fields[2])
            if fields[0] not in school_ranges:
                name = name_id_dict[fields[0]]
                school_ranges[name] ={key: (fields[5],fields[6])}
            else:
                school_ranges[name][key] = (fields[5],fields[6])
    return school_ranges

schoolranges = create_min_max_dict(csv)


def calculate_scores(inputs,grade_values, schoolranges):
    '''
    Computes range of points needed on entrance exam for each selective enrollment school using 2015 data
    Inputs:
        inputs: student variables
        grade_values: point system CPS uses to weight grades 
        csv: csv file with point ranges for each school by tier
    Returns:
        dictionary of ranges by school for student's tier and current points attained
    '''
    
    point_ranges = {}
    #check test scores are integers between 0 and 100
    assert inputs["readingTest"] <= 100 and inputs["readingTest"] >= 0, "Please enter valid number of points between 0 and 100"
    assert inputs["mathTest"] <= 100 and inputs["readingTest"] >= 0, "Please enter valid number of points between 0 and 100"
    test_scores = round(inputs["readingTest"] * 1.515) + round(inputs["mathTest"] * 1.515)
    grade_pts = grade_values[inputs["readingGrade"]] + grade_values[inputs["mathGrade"]] + grade_values[inputs["scienceGrade"]] + grade_values[inputs["socialGrade"]]
    total_pts = test_scores + grade_pts
    for school in schoolranges:
        t = "Tier" + str(inputs["tier"])

        print(school)
        print(schoolranges[school])

        max_ = int(schoolranges[school][t][1]) - total_pts
        min_ = int(schoolranges[school][t][0]) - total_pts
        point_ranges[school] = (min_,max_)
    return point_ranges
#print(schoolranges)

point_ranges = calculate_scores(inputs, grade_values, schoolranges)