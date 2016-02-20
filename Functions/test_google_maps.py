import csv
import google_maps

def create_dict():
	reader = csv.reader(open('../Clean Data/addresses.csv', 'r'), delimiter='|')
	d = {}
	for row in reader:
		k,v = row
		d[k] = v

	return d

def test_google_maps(d):
	for school1 in d:
		for school2 in d:
			print(google_maps.get_travel_info_transit(d[school1], d[school2]))
