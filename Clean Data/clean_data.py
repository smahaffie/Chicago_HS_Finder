import csv
import subprocess

'''
Contains all the commands to clean all of the csvs required to build the data base
'''

'''
Clean college enrollment and persistence data
'''

COMMAND = '''awk 'BEGIN {FS = "|"};{print $1"|"$3"|"$5"|"$10}' < 'Data_Files/collenrollpersist_rpt_20151025.csv' > 'Data_Files/CEP.csv' '''
subprocess.call(COMMAND, shell=True)
with open("Data_Files/CEP.csv",'r') as f, open("Data_Files/cleaned_CEP.csv",'w') as f1:
    next(f) # skip header line
    #next(f)
    #f1.write("School ID|Graduates|Enrollment Pct|Persistence Pct")
    for line in f:
        f1.write(line)



'''
Clean ACT data
'''

COMMAND = '''awk 'BEGIN {FS = "|"};{print $2"|"$4"|"$5"|"$7"|"$12"|"$17}' <'Data_Files/act_schools_2001_to_2015.csv' > 'Data_Files/ACT.csv' '''
subprocess.call(COMMAND, shell=True)
with open("Data_Files/ACT.csv", 'r') as f, open("Data_Files/cleaned_ACT.csv",'w') as f1:
    next(f)
    next(f)
    f1.write("School ID|Category|Category Type|Year|Composite Score Mean|Total Tested" + '\n')
    for line in f:
        f1.write(line)

'''
Clean freshman on track data
'''

COMMAND = '''awk 'BEGIN {FS = "|"};{print $1"|"$3"|"$4}' <'Data_Files/FOT_SchoolLevel_2015.csv' > 'Data_Files/FOT.csv' '''
subprocess.call(COMMAND, shell=True)
with open("Data_Files/FOT.csv", 'r') as f, open("Data_Files/cleaned_FOT.csv",'w') as f1:
    next(f)
    next(f)
    f1.write("School ID|On Track Rate|Total Number of Freshman" + '\n')
    for line in f:
        f1.write(line)

'''
Clean category and rating data contained in 3 csvs
'''

COMMAND = '''awk 'BEGIN {FS = "|"};{print $1"|"$2"|"$3"|"$5}' <'Data_Files/main_high_schools.csv' > 'Data_Files/Assessment912.csv' '''
subprocess.call(COMMAND, shell=True)
with open("Data_Files/Assessment912.csv", 'r') as f, open("Data_Files/cleaned_Assessment912.csv",'w') as f1:
    next(f)
    next(f)
    next(f)
    next(f)
    f1.write("School ID|School Name|Network|Rating" + '\n')
    for line in f:
        f1.write(line)

COMMAND = '''awk 'BEGIN {FS = "|"};{print $1"|"$2"|"$3"|"$9}' <'Data_Files/combo_high_schools.csv' > 'Data_Files/Assessmentcombo.csv' '''
subprocess.call(COMMAND, shell=True)
with open("Data_Files/Assessmentcombo.csv", 'r') as f, open("Data_Files/cleaned_Assessmentcombo.csv",'w') as f1:
    next(f)
    next(f)
    next(f)
    next(f)
    f1.write("School ID|School Name|Network|Rating" + '\n')
    for line in f:
        f1.write(line)

COMMAND = '''awk 'BEGIN {FS = "|"};{print $1"|"$2"|"$3"|"$5}' <'Data_Files/options_high_schools.csv' > 'Data_Files/Assessmentoptions.csv' '''
subprocess.call(COMMAND, shell=True)
with open("Data_Files/Assessmentoptions.csv", 'r') as f, open("Data_Files/cleaned_Assessmentoptions.csv",'w') as f1:
    next(f)
    next(f)
    next(f)
    next(f)
    f1.write("School ID|School Name|Network|Rating" + '\n')
    for line in f:
        f1.write(line)