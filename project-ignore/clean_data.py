import csv
import subprocess

def get_average(filename, column):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        total = length = 0
        for row in reader:
            try:
                x = row[column]
                total += float(x)
                length += 1
            except ValueError:
                pass
                #print("Error converting: {}".format(x))
    average = total / length
    return average

#COMMAND = """awk 'BEGIN {FS = ","};{print $1  "," $3 "," $5}' collenrollpersist_rpt_2015.csv"""

COMMAND = '''awk 'BEGIN {FS = ","};{print $1","$3","$5}' < 'collenrollpersist_rpt_2015.csv' > 'CEP.csv' '''
subprocess.call(COMMAND, shell=True)
with open("CEP.csv",'r') as f, open("cleaned_CEP.csv",'w') as f1:
    next(f) # skip header line
    for line in f:
        f1.write(line)

COMMAND = '''awk 'BEGIN {FS = ","};{print $1","$5","$8","$9","$11}' < 'eccc_all_schools_2015.csv' > 'ECCC.csv' '''
subprocess.call(COMMAND, shell = True)
with open("ECCC.csv",'r') as f, open("cleaned_ECCC.csv",'w') as f1:
    next(f)
    next(f)
    next(f)
    # skip header line
    for line in f:
        f1.write(line)
        break
    next(f)
    for line in f:
        f1.write(line)

COMMAND = '''awk 'BEGIN {FS = ","};{print $2","$4","$5","$7","$12","$17}' <'act_schools_2001_to_2015.csv' > 'ACT.csv' '''
subprocess.call(COMMAND, shell=True)
with open("ACT.csv", 'r') as f, open("cleaned_ACT.csv",'w') as f1:
    next(f)
    next(f)
    f1.write("School ID, Category, Category Type, Year, Composite Score Mean, Total Tested" + '\n')
    for line in f:
        f1.write(line)