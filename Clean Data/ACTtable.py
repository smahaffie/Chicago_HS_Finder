import sqlite3, csv

'''
Contains function to generate sql tables from csv files and compute average statistics
'''

def create(categoryofinterest):
    connection = sqlite3.connect('CHSF.db')
    c = connection.cursor()

    if categoryofinterest == 'ACT': 
        create = '''CREATE TABLE act
        (school_id varchar(8),
        category varchar(20),
        category_type varchar(20),
        year integer,
        composite_score_mean real,
        total_tested integer);'''
        #constraint pk_act school_id????
    elif categoryofinterest == 'CEP':
        create = '''CREATE TABLE cep
        (school_id varchar(8),
        graduates integer,
        enrollment_pct real);'''

    c.execute(create)
    connection.close()

def import_data(categoryofinterest):

    connection = sqlite3.connect('CHSF.db')
    c = connection.cursor()

    if categoryofinterest == 'ACT':
        with open('cleaned_ACT.csv', 'r') as fin:
            dr = csv.DictReader(fin)        
            to_db = [(i['School ID'], i[' Category'], i[' Category Type'], i[' Year'], i[' Composite Score Mean'], i[' Total Tested']) for i in dr]
        c.executemany("INSERT INTO act (school_id, category, category_type, year, composite_score_mean, total_tested) VALUES (?, ?, ?, ?, ?, ?);", to_db)

    elif categoryofinterest == 'CEP':
        with open('cleaned_CEP.csv', 'r') as fin:
            dr = csv.DictReader(fin)
            to_db = [(i['School ID'], i['Graduates'], i['Enrollment Pct']) for i in dr]            
        c.executemany("INSERT INTO cep (school_id, graduates, enrollment_pct) VALUES (?, ?, ?);", to_db)

def compute_average(categoryofinterest):
    connection = sqlite3.connect('CHSF.db')
    c = connection.cursor()

    if categoryofinterest == 'ACT':
        average = '''SELECT sum(total_tested*
            composite_score_mean)/sum(total_tested) AS average
            FROM act  WHERE year = 2015 AND category = "Overall" 
            AND category_type = "Overall";'''

    elif categoryofinterest == 'CEP':
        average = '''SELECT * FROM cep;'''
        # '''SELECT sum(graduates*enrollment_pct)/sum(graduates) AS average
         #   FROM cep;'''

    r = c.execute(average)
    connection.close()
    print(r.fetchall())

