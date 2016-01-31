'''function that takes NWEA Reading Percentile, NWEA Math Percentile, 
7th Grade Reading Grade, 7th Grade Math Grade,7th Grade Science Grade,
7th Grade Social Studies Grade, and tier and returns score range '''

import re
import util
import bs4
import csv

inputs = {"readingTest": 90, "mathTest": 90, "readingGrade": "A", "mathGrade": "B", "scienceGrade": "B+", "socialGrade": "A-", "tier": 1}
grade_values = {"A": 75, "B":50, "C": 25, "D": 0, "F":0 }
school_ranges = {"Brooks":{1:(602,739),2:(665,744),3:(690,746),4:655,}}
csv = 'Data/Cutoff_Scores_2015-2016.csv'

def create_min_max_dict(csv):
	school_ranges = {}
	with open(csv) as f:
		f.readline()
		for row in f:
			fields = row.strip().split(",")
			if fields[0] not in school_ranges:
				school_ranges[fields[0]] = {"".format(fields[1],fields[2])}




def calculate_scores(inputs,school_ranges, grade_values):
	point_ranges = {}
	#check test scores are integers between 0 and 100
	assert inputs[readingTest] <= 100 and inputs[readingTest] >= 0, "Please enter valid number of points between 0 and 100"
	assert inputs[mathTest] <= 100 and inputs[readingTest] >= 0, "Please enter valid number of points between 0 and 100"
	test_scores = round(inputs[readingTest] * 1.515) + round(inputs[mathTest] * 1.515)
	grade_pts = grade_values[readingGrade] + grade_values[mathGrade] + grade_values[scienceGrade] + grade_values[socialGrade]
	total_pts = test_scores + grade_pts
	for i in school_ranges:
		max_ = schoolranges[i][inputs[tier]][1] - total_pts
		min_ = schoolranges[i][inputs[tier]][0] - total_pts
		point_ranges[i] = (min_,max_)

