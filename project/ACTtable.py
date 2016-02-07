import sqlite3


connection = sqlite3.connect(WHAT HERE)
c = connection.cursor()

create = '''CREATE TABLE act
(school_id varchar(8),
category varchar(20),
category_type varchar(20),
year integer,
composite_score_mean real,
total_tested integer);'''

c.execute(create)


separate = '''.separator ","'''
imported = '''.import cleaned_ACT.csv act'''

average = '''SELECT sum(total_tested*
    composite_score_mean)/sum(total_tested) AS average
    FROM act  WHERE year = 2015 AND category = "Overall" 
    AND category_type = "Overall";'''
