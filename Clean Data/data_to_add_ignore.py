#create school name, ID csv

COMMAND = '''awk 'BEGIN {FS = ","};{print $1","$2"}' <'act_schools_2001_to_2015.csv' > 'ACT.csv' '''
subprocess.call(COMMAND, shell=True)
with open("ACT.csv", 'r') as f, open("cleaned_name_ID.csv",'w') as f1:
    next(f)
    next(f)
    f1.write("School name, School ID" + '\n')
    for line in f:
        f1.write(line)

#create category, ID csv






#create school name, ID table
  create_schoolnametable = " '''CREATE TABLE names (school_id varchar(8), name varchar(50));'''"

create_categorytable = "'''CREATE TABLE category (school id varchar(8), category varchar(50));'''"