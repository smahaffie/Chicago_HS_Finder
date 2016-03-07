#build_query.py

def build_query(neighborhood_schools, cleaned_data):
    '''
    Builds a SQL query based on user-inputs for schools to display in results
    Inputs:
        cleaned_data, Django form

    Returns:
        query, string
    '''
    
    neighborhood = False
    schooltypes = cleaned_data['schooltype']
    if 'Neighborhood' in schooltypes:
        schooltypes.remove('Neighborhood')
        neighborhood = True
    
    # If user checks no boxes, we will show them all school types. 
    if schooltypes == [] and neighborhood == False:
        neighborhood = True
        other_schooltypes = "('Selective Enrollment','Military Academy','Magnet','Contract','Special Needs','Charter')"

    elif len(schooltypes) == 1:
        other_schooltypes = "( '" + schooltypes[0] + "')"

    else:
        other_schooltypes = str(tuple(schooltypes))

    time_between = " "
    if cleaned_data["distance"] != None:
        seconds = int(cleaned_data["distance"]) * 60
        time_between = " AND ( time_between('{}', addrs.address) < {} )".format(str(cleaned_data['your_address'] + " Chicago, IL"),str(seconds))


    neighborhood_q_string = ''
    if neighborhood: #if user wants to see neighborhood schools
        neighborhood_q_string = ' OR (school_type = "Neighborhood" AND school_id IN (SELECT main.school_id ' + \
            'FROM main JOIN addrs on addrs.school_id = main.school_id WHERE main.school_id in ' + str(neighborhood_schools) + ")) "

  
    query = "SELECT addrs.address, main.name, main.school_id, main.school_type, act.composite_score_mean, main.rating, websites.website, " + "time_between('{}', addrs.address) / 60, ".format(cleaned_data['your_address'] + " Chicago, IL") + "cep.enrollment_pct, cep.persist_pct, ptroutes('{}', addrs.address)".format(cleaned_data['your_address']) + " FROM main  LEFT OUTER JOIN websites LEFT OUTER JOIN act LEFT OUTER JOIN cep JOIN addrs " + \
                "ON main.school_id = act.school_id  AND main.school_id = websites.school_id AND main.school_id = cep.school_id AND addrs.school_id = main.school_id" + \
                " WHERE act.category_type = 'Overall' AND act.year = '2015' AND (main.school_id in (SELECT school_id FROM main WHERE " + \
                ' (school_type IN ' + other_schooltypes + ")" + neighborhood_q_string + ")" + time_between + ");"       

    query_fot = "SELECT addrs.address, main.name, main.school_id, main.school_type, act.composite_score_mean, main.rating, websites.website, " + "time_between('{}', addrs.address) / 60, ".format(cleaned_data['your_address'] + " Chicago, IL") + "cep.enrollment_pct, cep.persist_pct, ptroutes('{}', addrs.address), fot.fot".format(cleaned_data['your_address']) + " FROM main LEFT OUTER JOIN fot LEFT OUTER JOIN websites LEFT OUTER JOIN act LEFT OUTER JOIN cep JOIN addrs " + \
                "ON main.school_id = act.school_id AND main.school_id = fot.school_id AND main.school_id = websites.school_id AND main.school_id = cep.school_id AND addrs.school_id = main.school_id" + \
                " WHERE act.category_type = 'Overall' AND act.year = '2015' AND (main.school_id in (SELECT school_id FROM main WHERE " + \
                ' (school_type IN ' + other_schooltypes + ")" + neighborhood_q_string + ")" + time_between + ");"    
    #minus google maps stuff for testing purposes
    '''temp =   "SELECT addrs.address, main.name, main.school_id, main.school_type, act.composite_score_mean, main.rating, " + "cep.enrollment_pct, cep.persist_pct FROM main LEFT OUTER JOIN act LEFT OUTER JOIN cep JOIN addrs " + \
            "ON main.school_id = act.school_id AND main.school_id = cep.school_id AND addrs.school_id = main.school_id" + \
            " WHERE act.category_type = 'Overall' AND act.year = '2015' AND (main.school_id in (SELECT school_id FROM main WHERE " + \
            ' (school_type IN ' + other_schooltypes + "))" + neighborhood_q_string + ");" '''
    return query_fot
    #return query