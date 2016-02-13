import google_maps 

def buildquery(home,maxtime):
	connection = sqlite3.connect('CHSF.db')
	c = connection.cursor()

	query = """SELECT  schoolname FROM test WHERE get_travel_info_transit(home,address) < maxtime """
	r = c.execute(query)
	results = r.fetchall()
	connection.close()
