'''Further clean categorization of schools data'''
files = ["cleaned_Assessmentoptions.csv", "cleaned_Assessmentcombo.csv", "cleaned_Assessment912.csv"]
magnets = ["DISNEY II HS", "VON STEUBEN HS", "CHICAGO AGRICULTURE HS", "CRANE MEDICAL HS", "DEVRY HS", "CURIE HS", "CLARK HS"]


def rename_categories(file,magnets):
    with open('file', 'r') as fin:
        dr = csv.DictReader(fin)
        for i in dr:
            if "Network" in i["Network"]:
                category = "Neighborhood"
            elif i["Network"] == "Service Leadership Academy":
                category = "Military Academy"
            elif i['School Name'] in magnets:
                category = "Magnet"
            if i["School Name"][-2:] == HS:
                name = i["School Name"][:-3].title() + "High School"
            else:
                name = i["School Name"].title() + "High School"
        to_db = [(i['School ID'], i['School Name'], category, i['Rating']) for i in dr]            


