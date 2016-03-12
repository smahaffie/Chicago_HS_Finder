import csv
import json

def create_min_max_dict(csv):
    '''
    Creates a json dictionary from csv file that lists points needed for each selective enrollment school by tier
    Inputs:
        csv, string filename with path
    Returns:
        json dictionary

    '''
    school_ranges = {}
    with open(csv,'r') as f:
        f.readline()
        for row in f:
            print(row)
            fields = row.strip().split(",")
            key = "{}{}".format(fields[1],fields[2])
            print(key)
            if name_id_dict[fields[0]] not in school_ranges:
                name = name_id_dict[fields[0]]
                school_ranges[name] ={key: (fields[5],fields[6])}
            else:
                print("add")
                school_ranges[name][key] = (fields[5],fields[6])

    with open("../Clean Data/Data_Files/school_ranges.json", 'w') as f:
        print(school_ranges)
        json.dump(school_ranges,f)
