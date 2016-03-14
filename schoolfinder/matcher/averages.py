'''
This file contains the code to to connect to the above generated database and
calculate the city wide act score, enrollment percentage, persistance 
percentage, and freshman on track
'''

import sqlite3

def calc_averages():
    '''
    Inputs:
        None

    Outputs:
        tuple containing city averages
    '''
    connection = sqlite3.connect('CHSF.db')
    c = connection.cursor()

    ACT_query = '''SELECT sum(total_tested*
    composite_score_mean)/sum(total_tested) AS average
    FROM act WHERE year = 2015 AND category = "Overall" 
    AND category_type = "Overall";'''

    r = c.execute(ACT_query)

    average_ACT = r.fetchall()
    average_ACT = average_ACT[0][0]

    EPCT_query = '''SELECT sum(graduates*
    enrollment_pct)/sum(graduates) FROM cep;'''

    r = c.execute(EPCT_query)
    average_epct = r.fetchall()
    average_epct = average_epct[0][0]

    PPCT_query = '''SELECT sum(graduates*persist_pct)
    /sum(graduates) FROM cep;'''

    r = c.execute(PPCT_query)
    average_ppct = r.fetchall()
    average_ppct = average_ppct[0][0]

    FOT_query = '''SELECT sum(numfresh*fot)/
    sum(numfresh) FROM fot;'''

    r = c.execute(FOT_query)
    average_on_track_rate = r.fetchall()
    average_on_track_rate = average_on_track_rate[0][0]

    return (average_on_track_rate, average_ppct, average_epct, average_ACT)
