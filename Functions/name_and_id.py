import csv

def make_id_to_name_dict():
    reader = csv.reader(open('../Clean Data/merged.csv', 'r'))
    id_to_name = {}
    for row in reader:
        id_to_name[row[0]] = row[1]

    return id_to_name

def make_name_to_id_dict():
    reader = csv.reader(open('../Clean Data/merged.csv', 'r'))
    name_to_id = {}
    for row in reader:
        name_to_id[row[1]] = row[0]

    return name_to_id

def get_schoolname(id, id_to_name):
    return id_to_name[id]

def get_id(schoolname, name_to_id):
    return name_to_id[schoolname]

