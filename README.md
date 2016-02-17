# 122project

Raw data:

act_schools_2001_to_2015.csv
Assessment_data_9_12_schools.csv
Assessment_data_comboschools.csv
Assessment_data_optionschools.csv
collenrollpersist_rpt_2015.csv
FOT_SchoolLevel_20151023.csv

Intermediate data (generated after intermediate cleaning using AWK) :

ACT.csv - ACT schools broken down by school and category
CEP.csv - College enrollment stats 
FOT.csv - Freshman on track stats
Assessment912.csv - contains school name, rating, and category 
Assessmentcombo.csv - contains school name, rating, and category 
Assessmentoptions.csv - contains school name, rating, and category 

cleaned_Assessment912.csv - cleaned but with incorrect labelling
cleaned_Assessmentcombo.csv - cleaned but with incorrect labelling
cleaned_Assessmentoptions.csv - cleaned but with incorrect labelling
cleaned_Assessment912_final.csv - correct labelling for types of schools
cleaned_Assessmentcombo_final.csv - correct labelling for types of schools
cleaned_Assessmentoptions_final.csv - correct labelling for types of schools

Cleaned data:

addresses.csv - maps school name to school address
cleaned_ACT.csv
cleaned_CEP.csv
cleaned_FOT.csv
merged.csv - merges the 3 cleaned_Assessment*_final.csv into 1 file


Scripts:

get_addresses.py - scrape CPS website to get a csv that maps school names to their geographic addresses
ACTable.py - contains code to generate ACT and CEP SQL tables and compute average ACT score and CEP value
clean_data.py - contains code to clean csv files 
clean_school_categories.py - takes the three files cleaned_Assesment* and relabels the 
school types using a hard-coded list of magnet and selective enrollment schools and relabels 
all school names with "High School" and makes approaching upper/lower case
schoolID_to_address.py
calculate_score.py - generate student points needed on entrance exam given grades and tier
get_neighborhood_schools.py - use CPS tool to generate neighborhood schools for a given address
get_tier_number.py - find tier that an address falls into
google_maps.py - find distance between two addresses
name_and_id.py - maps school names to ids

Database:
CHSF.db