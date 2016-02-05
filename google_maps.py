import googlemaps

def find_best_route(home, school, travel_mode):
    '''
    Inputs:
        home: address string
        school: address string

    Returns:
        json
    '''
    gmaps = googlemaps.Client(key='AIzaSyCHtXoboDd-gh-swjytgWi_JkO1ObYJJYM')
    directions_json = gmaps.directions(home, school, mode=travel_mode)
    best_route = directions_json[0]['legs'][0]

    return best_route

def get_travel_info_transit(home, school):
    '''
    Inputs:
        home: address string
        school: address string

    Returns:
        (trip duration in seconds, 
        time spent walking in seconds, 
        list of tuples of form (type, line/route name) for each public transportation route taken)
    '''
    best_route = find_best_route(home, school, 'transit')

    duration_text = best_route['duration']['text']
    duration = best_route['duration']['value']

    walking_time = 0 # in seconds
    ptroutes = []
    for step in best_route['steps']:
        if step['travel_mode'] == "WALKING":
            walking_time += step['duration']['value']
        elif step['travel_mode'] == 'TRANSIT':
            line = step['transit_details']['line']
            ptroutes.append((line['vehicle']['type'], line['short_name']))

    return duration, walking_time, ptroutes
