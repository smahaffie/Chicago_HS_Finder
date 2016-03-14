import csv
import json

'''
This file takes the csv we created that maps school names to addresses
and writes a new file that maps school IDs to addresses so that we
can import this data in SQLite with school ID as the primary key

This code is only necessary for building the initial database

Original code
'''
#we ran this function with filenames Data_Files/id_to_name.json and Data_Files/name_to_address.json

def make_id_to_address(name_to_address_json,id_to_name_json):
	'''uses extant id_to_name and name_to_address dictionaries to 
	match school id's with their addresses and creates a csv file
	with the matched pairs

	Inputs:
		name_to_address_json, json file
		id_to_name_json, json file

	Side effects:
		id_to_address.csv, csv file
	'''

	with open(name_to_address_json,'r') as f:
		name_to_address = json.load(f)

	with open(id_to_name_json,'r') as f:
		id_to_name = json.load(f)

	with open('Data_Files/id_to_address.csv', 'w', newline = '') as csvfile:
		w = csv.writer(csvfile)
		for sid in id_to_name:
			name = id_to_name[sid].upper()
			if name not in name_to_address:
				if name[-11:] == 'HIGH SCHOOL':
					if name[:-11] + "HS" in name_to_address:
						name = name[:-11] + 'HS'
					elif name[:-12] in name_to_address:
						name = name[:-12]
			assert name in name_to_address
			w.writerow([sid, name_to_address[name]])
 

