import csv

def make_id_to_name_dict():
    '''function that creates id_to_name dictionary,
    with school ids as keys and names of schools as values'''
    reader = csv.reader(open('../Clean Data/merged.csv', 'r'))
    id_to_name = {}
    for row in reader:
        id_to_name[row[0]] = row[1]

    return id_to_name

def make_name_to_id_dict():
    '''function that creates name_to_id dictionary, with
    school name as the key and school_id as the value'''
    reader = csv.reader(open('../Clean Data/merged.csv', 'r'))
    name_to_id = {}
    for row in reader:
        name_to_id[row[1]] = row[0]

    return name_to_id

def get_schoolname(id, id_to_name):
    '''given an id and the id_to_name dictionary,
    return the school's name'''
    return id_to_name[id]

def get_id(schoolname, name_to_id):
    '''given a school's name and the name_to_id dictionary,
    return the school's id'''
    return name_to_id[schoolname]

