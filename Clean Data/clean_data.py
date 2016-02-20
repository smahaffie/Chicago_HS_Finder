import csv
import subprocess

'''
Contains all the commands to clean all of the csvs required to build the data base
'''

'''
Clean college enrollment and persistence data
'''

COMMAND = '''awk 'BEGIN {FS = "|"};{print $1","$3","$5","$10}' < 'collenrollpersist_rpt_20151025.csv' > 'CEP.csv' '''
subprocess.call(COMMAND, shell=True)
with open("CEP.csv",'r') as f, open("cleaned_CEP.csv",'w') as f1:
    next(f) # skip header line
    f1.write("School ID, Graduates, Enrollment Pct, Persistence Pct")
    for line in f:
        f1.write(line)



'''
Clean ACT data
'''

COMMAND = '''awk 'BEGIN {FS = "|"};{print $2","$4","$5","$7","$12","$17}' <'act_schools_2001_to_2015.csv' > 'ACT.csv' '''
subprocess.call(COMMAND, shell=True)
with open("ACT.csv", 'r') as f, open("cleaned_ACT.csv",'w') as f1:
    next(f)
    next(f)
    f1.write("School ID, Category, Category Type, Year, Composite Score Mean, Total Tested" + '\n')
    for line in f:
        f1.write(line)

'''
Clean freshman on track data
'''

COMMAND = '''awk 'BEGIN {FS = "|"};{print $1","$3", "$4}' <'FOT_SchoolLevel_2015.csv' > 'FOT.csv' '''
subprocess.call(COMMAND, shell=True)
with open("FOT.csv", 'r') as f, open("cleaned_FOT.csv",'w') as f1:
    next(f)
    next(f)
    f1.write("School ID, On Track Rate, Total Number of Freshman" + '\n')
    for line in f:
        f1.write(line)

'''
Clean category and rating data contained in 3 csvs
'''

COMMAND = '''awk 'BEGIN {FS = "|"};{print $1","$2","$3", "$5}' <'main_high_schools.csv' > 'Assessment912.csv' '''
subprocess.call(COMMAND, shell=True)
with open("Assessment912.csv", 'r') as f, open("cleaned_Assessment912.csv",'w') as f1:
    next(f)
    next(f)
    next(f)
    next(f)
    f1.write("School ID, School Name, Network, Rating" + '\n')
    for line in f:
        f1.write(line)

COMMAND = '''awk 'BEGIN {FS = "|"};{print $1","$2","$3", "$9}' <'combo_high_schools.csv' > 'Assessmentcombo.csv' '''
subprocess.call(COMMAND, shell=True)
with open("Assessmentcombo.csv", 'r') as f, open("cleaned_Assessmentcombo.csv",'w') as f1:
    next(f)
    next(f)
    next(f)
    next(f)
    f1.write("School ID, School Name, Network, Rating" + '\n')
    for line in f:
        f1.write(line)

COMMAND = '''awk 'BEGIN {FS = "|"};{print $1","$2","$3", "$5}' <'options_high_schools.csv' > 'Assessmentoptions.csv' '''
subprocess.call(COMMAND, shell=True)
with open("Assessmentoptions.csv", 'r') as f, open("cleaned_Assessmentoptions.csv",'w') as f1:
    next(f)
    next(f)
    next(f)
    next(f)
    f1.write("School ID, School Name, Network, Rating" + '\n')
    for line in f:
        f1.write(line)