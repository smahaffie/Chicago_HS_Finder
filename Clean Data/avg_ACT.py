import sqlite3

def compute_average(categoryofinterest):
    connection = sqlite3.connect('CHSF.db')
    c = connection.cursor()

    if categoryofinterest == 'ACT':
        average = '''SELECT sum(total_tested*
            composite_score_mean)/sum(total_tested) AS average
            FROM act  WHERE year = 2015 AND category = "Overall" 
            AND category_type = "Overall";'''

    r = c.execute(average)



    connection.close()

    print(r.fetchall())