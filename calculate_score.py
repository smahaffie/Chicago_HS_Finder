'''function that takes NWEA Reading Percentile, NWEA Math Percentile, 
7th Grade Reading Grade, 7th Grade Math Grade,7th Grade Science Grade,
7th Grade Social Studies Grade, and tier and returns score range 

name = "readingTest"
name = "mathTest"
name = "readingGrade"
name = "mathGrade"
name = "scienceGrade"
name = "socialGrade"
name = "tier"

import requests
data = {'readingTest':80,'mathTest':90,'readingGrade':'A','mathGrade':'B',
'scienceGrade':'A-','socialGrade':'B+','tier':1}

url = "http://www.cpsoae.org/apps/pages/index.jsp?uREC_ID=72696&type=d&termREC_ID&pREC_ID=545282"

r = requests.post(url, params = data )
print(r.content)

'''
import urllib
import requests
import util

url = "http://www.cpsoae.org/apps/pages/index.jsp?uREC_ID=72696&type=d&termREC_ID&pREC_ID=545282"

url2 = util.get_request(url)


form_data = {'readingTest':80,'mathTest':90,'readingGrade':'A','mathGrade':'B',
'scienceGrade':'A-','socialGrade':'B+','tier':1}

params = urllib.parse.urlencode(form_data)
req = urllib.request.request(url,params)
response = urllib.request.urlopen(req)
data = response.read()



'''

br = mechanize.Browser()
br.set_all_readonly(False)    # allow everything to be written to
br.set_handle_robots(False)   # ignore robots
br.set_handle_refresh(False)
response = br.open(url)

for form in br.forms():
    print("Form name:", form.name)
    print(form)'''