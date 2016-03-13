'''
This file contains the function that generates a json file to store
 the data on the minimum and maximum points needed for entry to each 
 selective enrollment school by tier. This is data that only needs to 
 be generated once per year (it is not student specific). 
'''

import csv
import json

def create_min_max_dict(csv):
    '''
    Creates a json dictionary from csv file that lists points needed for each selective enrollment school by tier
    Inputs:
        csv, string filename with path
    Returns:
        json file

    '''
    school_ranges = {}
    with open(csv,'r') as f:
        f.readline()
        for row in f:
            fields = row.strip().split(",")
            key = "{}{}".format(fields[1],fields[2]) #keys are the tier 

            if name_id_dict[fields[0]] not in school_ranges:
                name = name_id_dict[fields[0]]
                school_ranges[name] ={key: (fields[5],fields[6])}
                
            else:
                school_ranges[name][key] = (fields[5],fields[6])

    with open("Data_Files/school_ranges.json", 'w') as f:
        json.dump(school_ranges,f)
