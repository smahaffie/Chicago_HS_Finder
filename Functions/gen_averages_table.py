'''
SQL code to calculate average scores for various metrics and store them in a seperate TABLE
This code only needs to be run whenever data on schools in updated in the database 
'''
import sqlite3
import math

from calculate_score import point_ranges, schoolranges

mult_dict = {1:0.1, 2:0.4, 3:0.6, 4:0.8, 5:1, 6:1.2, 7:1.4, 8:1.6, 9:1.8, 10:2.1}

#INCLUDE PROPER DATABASE LOCATION BELOW
connection = sqlite3.connect('../schoolfinder/CHSF.db')
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

gen_average_table = '''CREATE TABLE averages (
    statistic varchar(10),
    average float(6));
    INSERT INTO averages (statistic, average),
    VALUES ('FOT', ?), ('PPCT', ?), ('EPCT', ?), ('ACT', ?)'''

r = c.execute(gen_average_table, (average_on_track_rate, average_ppct, average_epct, average_ACT))

