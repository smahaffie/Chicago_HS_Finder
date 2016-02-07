import requests
import bs4

def get():
    r = requests.get("http://schoolinfo.cps.edu/schoolprofile/SearchResults.aspx")
    text = r.text
    soup = bs4.BeautifulSoup(text, 'html5lib')

    tags = soup.find_all('table')
    for tag in tags:
        if tag.has_attr('class'):
            if tag['class'] == ['table', 'table-condensed']:
                table = tag

    table_soup = bs4.BeautifulSoup(table.text, 'html5lib')
    body = table_soup.find('body')
    body_soup = bs4.BeautifulSoup(body.text, 'html5lib')

    return body_soup

#iframe resizer???????