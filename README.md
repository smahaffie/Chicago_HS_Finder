# 122project

Libraries to install:
Googlemaps
Selenium

Instructions to recreate database:
run clean_data.py to generate first set of cleaned files
run clean_school_categories.py to generate second set of cleaned files
Copy and paste text in gen_table.txt to create sql tables
import cleaned_FOT.csv, cleaned_ACT.csv, merged.csv, addresses.csv, and cleaned_CEP. csv 
using sqlite ".seperator "|" and ".import <filename>"


Raw data in Clean Data/Data Files:

act_schools_2001_to_2015.csv, ACT scores data
Assessment912.csv
Assessmentcombo.csv
Assessmentoptions.csv
collenrollpersist_rpt_2015.csv
FOT_SchoolLevel_2015.csv, Freshman-on-track data
CPS_SchoolsView.csv, school website list


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
IEP_schools.csv - list of schools with IEP programs
id_to_address.csv - list of school ids and school addresses
school_ranges.json - maps selective enrollment schools to the min and max points for admission in 2015

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
ranking.py - calculate ranking for a SQL to be displayed in results page


Database:
CHSF.db

Tables:
ACT - average ACT scores for 2015 including divisions by race, program, etc.
CEP - college enrollment and persistence rates for 2015\
addrs - school ID and school address
main - school ID, school name, school category, school rating
FOT - freshman on track rates and number of freshman by school
