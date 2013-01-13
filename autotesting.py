from bs4 import BeautifulSoup
import requests
import urllib
domain = "asos.com"
search = requests.get("https://www.google.com/search?q=site%3A"+urllib.quote(domain, ""))
soup = BeautifulSoup(search.text)
#print search.text
output = []
for link in soup.find_all('a'):
    snippet = link.get('href')
    if "www.%s" % (domain) in snippet and 'url?q=' in snippet:
        snippet = snippet[7:]
        snippet = snippet[:snippet.find('&sa=')]
        output.append(snippet)
#print output
destination = output[2]
affiliate_link = 'http://ad.zanox.com/ppc/?22484574C16048796T&ULP=[[[URL]]]&zpar0=[tracking]'
url = affiliate_link.replace('[tracking]','skim1x2')
network_id = 20
if network_id == 2:
    url = url.replace('[URLenc]', urllib.quote(urllib.quote(destination, "")))
elif network_id == 9:
    page = destination[page.find('/')+1:]
    url = url.replace('[URLnodomain]', page)
else:
    url = url.replace('[URLenc]', urllib.quote(destination, ""))
    url = url.replace('[URL]', urllib.quote(destination, ""))
print destination
print url