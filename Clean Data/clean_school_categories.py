'''Further clean categorization of schools data'''
import csv
import pandas as pd
csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)

files = ["Data_Files/cleaned_Assessmentoptions.csv", "Data_Files/cleaned_Assessmentcombo.csv", "Data_Files/cleaned_Assessment912.csv"]
magnets = ["DISNEY II HS", "VON STEUBEN HS", "CHICAGO AGRICULTURE HS", "CRANE MEDICAL HS", "DEVRY HS", "CURIE HS", "CLARK HS"]
se = ["BROOKS HS", "JONES HS", "KING HS", "LANE TECH HS", "LINDBLOM HS", "NORTHSIDE PREP HS", "PAYTON HS", "SOUTH SHORE INTL HS", "WESTINGHOUSE HS", "YOUNG HS" ]
IB_schools = ["Amundsen High School","Back of the Yards High School",
"Bogan High School", "Bronzeville Scholastic Academy High School", "Clemente High School",
"Curie Metropolitan High School", "Farragut High School","Hubbard High School", 
"Hyde Park Academy High School","Juarez High School","Kelly High School","Kennedy High School",
"Lincoln Park High School","Morgan Park High School",
"The Ogden International School of Chicago","Prosser Career Academy","Schurz High School",
"Senn High School","South Shore International","Steinmetz Academic Centre",
"Taft High School","Washington High School"]

def rename_categories(files,magnets,se):
    for f in files:
        print(f)
        new = f[:-4] + "_final.csv"
        with open(f) as fin, open(new, 'w') as f1:
            dr = csv.DictReader(fin,fieldnames=["School ID","School Name","Network","Rating"],dialect = "piper")
            writer = csv.writer(f1,delimiter = "|")
            next(fin)
            for i in dr:
                if i["Network"] == None:
                    print(i)
                category = i["Network"].title()
                if "NETWORK" in i["Network"]:
                    category = "Neighborhood"
                if i["Network"] == "SERVICE LEADERSHIP ACADEMIES":
                    category = "Military Academy"
                if i["Network"] == "Os4" or i["Network"] == "Ausl":
                    category = "Reinvestment"
                if i['School Name'] in magnets:
                    category = "Magnet"
                if i['School Name'] in se:
                    category = "Selective Enrollment"
                if i["School Name"][-2:] == "HS":
                    name = i["School Name"][:-3].title() + " High School"
                else:
                    name = i["School Name"].title() + " High School"
               
                line = [i['School ID'],name, category, str(i['Rating'])]            
                writer.writerow(line)

#combine the seperate csvs
to_merge = ["Data_Files/cleaned_Assessmentoptions.csv", "Data_Files/cleaned_Assessmentcombo.csv", "Data_Files/cleaned_Assessment912.csv"]
merge = ["Data_Files/cleaned_Assessmentoptions_final.csv", "Data_Files/cleaned_Assessmentcombo_final.csv", "Data_Files/cleaned_Assessment912_final.csv"]
def merge_category_csvs(files):
    merged = open("merged.csv", 'w')
    merged.write("School ID|School Name|Network|Rating" + '\n')
    for f in files:
        with open(f,'r') as fil:
            for line in fil:
                print(line)
                merged.write(line)

def every_school_in_every_file(merged_file, list_of_incomplete_files, list_of_destinations ):
    '''ensures that every file in list of file has an entry
    for each school ID in merged by inputting null entry if not
    already present'''

    merged_df = pd.read_csv(merged_file, sep = '|')
    merged = [school for school in list(merged_df['School ID'])]
    print(len(merged))
    n=0
    for filename in list_of_incomplete_files:
        incomplete_df = pd.read_csv(filename, sep = '|')
        incomplete = [school for school in list(incomplete_df['School ID'])]
        print(len(incomplete))
        missing = [school for school in merged if not school in incomplete]
        print(len(missing))
        #missing_schools = {}
        for school in missing:
            s2 = pd.Series([school, None, None, None], index = list(incomplete_df.columns))
            incomplete_df.append(s2, ignore_index=True)
            #print(school)
        incomplete_df.to_csv(list_of_destinations[n], sep = '|')
        n+=1
        print(incomplete_df.shape)
#code to create SQL table

create = '''CREATE TABLE main
        (school_id varchar(8),
        name varchar(30),
        school_type varchar(30),
        rating varchar(3));'''