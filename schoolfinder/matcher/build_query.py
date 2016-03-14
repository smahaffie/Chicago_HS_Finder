# original

# This file contains the function that uses user inputs to build the main 
# SQL query

#there is no CSV that indicates whether a school has an IB program, so we 
#created this list from the list on the CPS website

IB_schools = ["Amundsen High School","Back of the Yards High School",
"Bogan High School", "Bronzeville Scholastic Academy High School", 
"Clemente High School","Curie Metropolitan High School", "Farragut High School",
"Hubbard High School", "Hyde Park Academy High School","Juarez High School",
"Kelly High School","Kennedy High School","Lincoln Park High School",
"Morgan Park High School","The Ogden International School of Chicago High School",
"Prosser Career Academy High School","Schurz High School","Senn High School",
"South Shore International  High School","Steinmetz Academic Centre  High School",
"Taft High School","Washington High School"]


def build_query(neighborhood_schools, cleaned_data):
    '''
    Builds a SQL query based on user-inputs for schools to display in results
    
    Inputs:
        cleaned_data, Django form
        neighborhood_schools, list of user's zoned neighborhood schools 

    Returns:
        query, string
    '''
    
    neighborhood = False
    schooltypes = cleaned_data['schooltype']



    #If the user is interested in IB schools, the ranking function considers all 
    #schools with IB programs, even if they are neighborhood schools as being
    #options that are open to them

    IB = " "

    if "International Baccalaureate" in schooltypes:
        IB = " OR ( main.name in " + str(tuple(IB_schools)) + ")"


    if 'Neighborhood' in schooltypes:
        schooltypes.remove('Neighborhood')
        neighborhood = True
    
    # If user checks no boxes, we will show them all school types. 
    if schooltypes == [] and neighborhood == False:
        neighborhood = True
        other_schooltypes = "('Selective Enrollment','Military Academy'," + \
            "'Magnet','Contract','Special Needs','Charter')"

    elif len(schooltypes) == 1:
        other_schooltypes = "( '" + schooltypes[0] + "')"

    else:
        other_schooltypes = str(tuple(schooltypes))

    time_between = " " # in case user does not specify a max distance
    if cleaned_data["distance"] != None:
        seconds = int(cleaned_data["distance"]) * 60
        time_between = \
            " AND ( time_between('{}', addrs.address) < {})".format(str(
                cleaned_data['your_address'] + " Chicago, IL"), str(seconds))


    neighborhood_q_string = ''
    if neighborhood: #if user wants to see neighborhood schools
        neighborhood_q_string = ' OR (school_type = "Neighborhood" AND ' + \
            'school_id IN (SELECT main.school_id ' + \
            'FROM main JOIN addrs on addrs.school_id = main.school_id WHERE '+\
            'main.school_id in ' + str(neighborhood_schools) + ")) "

    query = "SELECT addrs.address, main.name, main.school_id," + \
        " main.school_type, act.composite_score_mean, main.rating," + \
        " websites.website, get_transit_info('{}', addrs.address), ".format(
            cleaned_data['your_address'] + " Chicago, IL") + \
        "cep.enrollment_pct, cep.persist_pct, fot.fot" + \
        " FROM main LEFT OUTER JOIN fot LEFT OUTER JOIN websites " + \
        "LEFT OUTER JOIN act LEFT OUTER JOIN cep JOIN addrs " + \
        "ON main.school_id = act.school_id AND main.school_id = " + \
        " fot.school_id AND main.school_id = websites.school_id AND " + \
        "main.school_id = cep.school_id AND addrs.school_id = main.school_id"+\
        " WHERE act.category_type = 'Overall' AND act.year = '2015' AND " + \
        "(main.school_id in (SELECT school_id FROM main WHERE " + \
        ' (school_type IN ' + other_schooltypes + ")" + \
        neighborhood_q_string + ")" + IB + time_between + ");"
    
    return query
