
import util
import bs4
#scrape Chicago magazine high school rankings

url = "http://www.chicagomag.com/Chicago-Magazine/September-2014/Chicago-schools/Private-schools/"
request = util.get_request(url)
actual_url = util.get_request_url(request)

url = util.convert_if_relative_url(actual_url, url)
url = util.remove_fragment(url)



text = util.read_request(request)

soup = bs4.BeautifulSoup(text, 'html5lib')

tags = soup.find_all('tbody')
print(tags)