from bs4 import BeautifulSoup
import requests
import urllib
import mysql.connector
import password

def domain_extract(merchant_id):
    cnx = mysql.connector.connect(user=password.user, password=password.password, host=password.host, database=password.database)
    cursor = cnx.cursor()
    cursor.execute(("select id, merchant_id, domain from mugic_merchants_domains where merchant_id = %s") % (merchant_id))
    domain_list = cursor.fetchall()
    cursor.close()
    cnx.close()
    for domain in domain_list:
        print domain

def deeplink_extract(domain):
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
    return output

def create_affiliate_link(network_deeplink, destination):
    url = network_deeplink.replace('[tracking]', 'skim1x2')
    network_id = 20
    if network_id == 2:
        url = url.replace('[URLenc]', urllib.quote(urllib.quote(destination, "")))
    elif network_id == 9:
        page = destination[page.find('/')+1:]
        url = url.replace('[URLnodomain]', page)
    else:
        url = url.replace('[URLenc]', urllib.quote(destination, ""))
        url = url.replace('[URL]', urllib.quote(destination, ""))
    return url

if __name__ == '__main__':
    merchant_id = 1
    domain = "asos.com"
    network_deeplink = 'http://ad.zanox.com/ppc/?22484574C16048796T&ULP=[[[URL]]]&zpar0=[tracking]'
    domain = domain_extract(merchant_id)
    #output = deeplink_extract(domain)
    #destination = output[2]
    #affiliate_link = create_affiliate_link(network_deeplink, destination)
    #print destination
    #print affiliate_link
    