# 122project
 
Overview:
This project uses public data on Chicago Public Schools and user inputted-background and preferences to generate a list of schools that meet the user’s specifications and are ranked based on academic criteria and distance from the user’s home.

The data we use comes almost exclusively from http://cps.edu/SchoolData/Pages/SchoolData.aspx. 

Libraries to install:
Googlemaps: pip3 install -U googlemaps
Selenium: pip3 install selenium
Pandas: pip3 install pandas
Json: pip3 install json
Subprocess: pip3 install subprocess 

To run our application:
Navigate to Chicago_HS_Finder/schoolfinder/. 
Then enter the following in the terminal:
    $ python3 manage.py runserver
Open firefox and go to  http://127.0.0.1:8000/. Fill in the form with sample user preferences and press submit. Depending on the preferences that you enter, 1 or 2 Firefox windows may open and close within a few seconds. 
You should then be directed to a new page that shows a table displaying information on the 15 best schools for the user in ranked order based on the inputted preferences and our ranking algorithm. Each label corresponds to a label on the map, and each school’s name links to that school’s website. 

Please note that because we did not purchase a google maps api key, our free key stops working for up to several hours if it is queried too often. After this point, every query will redirect to an error page rather than to a results map and table. Therefore, if you plan to run many queries consecutively, it may be a good idea to check only a few school types at once, and especially to avoid when possible checking "Charter" and "IB" on multiple consecutive queries simply because of the large number of these schools for which students are eligible. In practice, we would purchase a real google maps key and we would not encounter this issue. 

Please also note, especially when entering addresses on the South Side, that for many of the school types, all of the schools are more than an hour away by public transportation. Therefore, to see the most interesting and useful results, it may be best to put in around 90 minutes as a furthest willingness to travel.

As an example, by running the following query with different importances assigned to transit time and academics, and different academic histories, you can observe the different results our algorithm returns: 

‘6031 S Ellis Ave’, 90 minutes, [Neighborhood, Selective Enrollment, Magnet, Contract]

Note that when the user checks that you are interested in IB schools, all of the schools of every type that offer IB programs will be eligible to be in the final list in addition to the schools of the types selected by the user.

Overall structure of our code:

The files in Clean Data contains the code that we used to clean the data that is stored in the SQLite database CHSF which is located in the schoolfinder folder. The subfolder Data_Files contains all the csvs involved in the data cleaning process (raw files, intermediate files, and final files that we imported in the database). We also cleaned data further using SQLite commands because we found it very easy to do and foolproof, so the final csvs do not correspond exactly to the entries in our database.
The folder schoolfinder contains all of the files that are integrated with our Django interface. The majority of the files that deal with our school selection and ranking algorithms are located in the matcher folder inside schoolfinder.  

Database:

The database contains various sets of data on every high school in Chicago. The key school_id is the primary key for all the tables except for the averages table. 

ACT - school ID, mean composite ACT scores for each school for 2011 thru 2015 including additional rows for scores for subsets of every school (by race, free/reduced lunch, etc.), and number tests for the set or subset
CEP - school ID, college enrollment and persistence rates for 2015, number of graduates
addrs - school ID and school address (contains all CPS schools)
main - school ID, school name, school category, school CPS-assigned rating
FOT - school ID, freshman on track rate, and number of freshman
websites - school id and website address (contains all CPS schools)
averages - statistic (mean act score, college enrollment rate, etc.) and its corresponding city-wide average for 2015 based on the entries in our database

The file gen_table.txt contains the SQL code that we used to create the tables in sqlite. We then used the .import command to import the csvs directly into the SQL tables. All of our files are bar-delimited. 

Raw data in Clean Data/Data Files:

act_schools_2001_to_2015.csv, ACT scores data
Assessment912.csv
Assessmentcombo.csv
Assessmentoptions.csv
collenrollpersist_rpt_2015.csv
FOT_SchoolLevel_2015.csv, Freshman-on-track data
CPS_SchoolsView.csv, school website list
Cutoff_Scores_2015_2016.csv - min and max scores for admissions to selective enrollment high schools


Intermediate data (generated after intermediate cleaned in some way, but not ready for import to sqlite) :

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
Combo_high_schools.csv - more intermediate cleaning
CPS_SchoolsView_cleaned.csv - more intermediate cleaning
Main_high_schools.csv - more intermediate cleaning
Options_high_schools.csv - more intermediate cleaning

Cleaned data (actually used in database or in files run through django):

addresses.csv - maps school name to school address
cleaned_ACT.csv - all data imported to act table in sqlite database
cleaned_CEP.csv - all data imported to cep table in sqlite database
cleaned_FOT.csv - all data imported to FOT table in sqlite database
merged.csv - merges the 3 cleaned_Assessment*_final.csv into 1 file; this file was used to create the main table in the sqlite database but we further cleaned the data in sqlite because it is very simple and less error-prone this way
IEP_schools.csv - list of schools with IEP programs
id_to_address.csv - list of school ids and school addresses
school_ranges.json - maps selective enrollment schools to the min and max points for admission in 2015
CPS_SchoolsView_cleaned.csv - maps school IDS to web addresses
Websites.json - above file in JSON form for easy use

Scripts:

Scripts associated with cleaning data or getting data:

averages.py - contains code to calculate citywide averages for act score, enrollment pct, persistant pct, and freshman on track rate
clean_data.py - contains code to clean csv files
clean_school_categories.py - takes the three files cleaned_Assesment* and relabels the
school types using a hard-coded list of magnet and selective enrollment schools and relabels
all school names with "High School" and makes approaching upper/lower case
get_addresses.py - scrape CPS website to get a csv that maps school names to their geographic addresses
make_id_to_address.py - makes dictionary matching school IDs to addresses
min_max_selective_enrollment.py - returns tuple of minimum and maximum points needed on CPS formula to gain entry to the selective enrollment school
name_and_id.py - maps school names to ids

Scripts that interact with user inputs:

get_neighborhood_schools.py - use CPS tool (http://cps.edu/ScriptLibrary/Map-SchoolLocator2015/index.html) to generate neighborhood schools for a given address
get_tier.py - find tier that an address falls into using http://cpstiers.opencityapps.org/ 
google_maps.py - find distance between two addresses
build_query .py - takes in user inputs to build query to select matching schools that are then ranked
Transit_info.py - contains all the functions that use the Google maps API to find information about travel time to every school
Views.py - processes all the requests made through django to call the appropriate functions and generate the appropriate templates
ranking.py - calculate ranking for a SQL to be displayed in results page

Django templates:

About.html - about page that explains how we generate our results
Error.html - this page appears if there is an error in the SQL query
Results.html - this page displays the schools that we suggest to the user
Start.html - this page is the home page that displays the form that asks the user for school preferences and address
