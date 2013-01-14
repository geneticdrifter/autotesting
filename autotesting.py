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
    return domain_list

def get_tracking_link(merchant_id):
    cnx = mysql.connector.connect(user=password.user, password=password.password, host=password.host, database=password.database)
    cursor = cnx.cursor()
    cursor.execute(("select network_deeplink from mugic_merchant where id = %s") % (merchant_id))
    network_deeplink = cursor.fetchall()
    cursor.close()
    cnx.close()
    return network_deeplink

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

def create_affiliate_link(tracking_url, destination):
    url = tracking_url.replace('[tracking]', 'skim1x2')
    network_id = 20
    if network_id == 2:
        url = url.replace('[URLenc]', urllib.quote(urllib.quote(destination, ""), ""))
    elif network_id == 9:
        page = destination[page.find('/')+1:]
        url = url.replace('[URLnodomain]', page)
    else:
        url = url.replace('[URLenc]', urllib.quote(destination, ""))
        url = url.replace('[URL]', urllib.quote(destination, ""))
    return url

if __name__ == '__main__':
    #merchant_id = raw_input("Give me a merchant ID")
    merchant_id = 27909
    merchant_info = domain_extract(merchant_id)
    tracking_url = get_tracking_link(merchant_id)
    domain = merchant_info[0][2]
    output = deeplink_extract(domain)
    destination = output[2]
    affiliate_link = create_affiliate_link(tracking_url, destination)
    print destination
    print affiliate_link