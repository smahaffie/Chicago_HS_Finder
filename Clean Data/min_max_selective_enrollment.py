import csv
import json

#inputs just for testing
csv = 'Data_Files/Cutoff_Scores_2015_2016'


name_id_dict = {'King':609751, 'Brooks':609726, 'Hancock':609694, 'Jones': 609678, 'Lane':609720, 'Lindblom': 610391,
'Northside':609749, 'Payton':609680, 'South Shore':610547, 'Westinghouse':609693, 'Young':609755}


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

    with open("Data_Files/school_ranges.json", 'w') as f:
        print(school_ranges)
        json.dump(school_ranges,f)
