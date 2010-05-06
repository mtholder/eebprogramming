from BeautifulSoup import BeautifulSoup
import re
import urllib2

url = 'http://blogsearch.google.com/blogsearch?q=python'
response = urllib2.urlopen(url)
html = response.read()
#print html
soup = BeautifulSoup(html)
links = soup.findAll('a', id=re.compile("^p-"))
for link in links:
    print link['href']
