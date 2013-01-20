from bs4 import BeautifulSoup
import requests
import urllib
import mysql.connector
import password
import sys
import csv

LINKSHARE = 2
PAIDONRESULTS = 9

def merchant_query(merchant_id):
    cnx = mysql.connector.connect(user=password.user, password=password.password, host=password.host, database=password.database)
    cursor = cnx.cursor()
    cursor.execute("select md.id, md.merchant_id, md.domain, mm.network_deeplink, mm.network_id from mugic_merchants_domains md inner join mugic_merchant mm on mm.id = md.merchant_id where md.merchant_id = %s" , (merchant_id,))
    merchant_information = cursor.fetchall()
    cursor.close()
    cnx.close()
    return merchant_information

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

def create_affiliate_link(tracking_url, destination, network_id):
    url = tracking_url.replace('[tracking]', 'skim1x2')
    if network_id == LINKSHARE:
        url = url.replace('[URLenc]', urllib.quote(urllib.quote(destination, ""), ""))
    elif network_id == PAIDONRESULTS:
        destination = destination.replace('http://', '')
        destination = destination[destination.find('/')+1:]
        url = url.replace('[URLnodomain]', destination)
    else:
        url = url.replace('[URLenc]', urllib.quote(destination, ""))
        url = url.replace('[URL]', urllib.quote(destination, ""))
    return url

if __name__ == '__main__':
    merchant_ids = sys.argv[1:]
    with open('links.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['merchant ID'] + ['domain'] + ['network ID'] + ['link'] + ['affiliate link'])
        for merchant_id in merchant_ids:
            merchant_info = merchant_query(merchant_id)
            domain = merchant_info[0][2]
            deeplinks = deeplink_extract(domain)
            for link in deeplinks:
                tracking_url = merchant_info[0][3]
                network_id = merchant_info[0][4]
                affiliate_link = create_affiliate_link(tracking_url, link, network_id)
                writer.writerow([merchant_id] + [domain] + [network_id] + [link] + [affiliate_link])