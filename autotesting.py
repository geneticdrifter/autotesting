from bs4 import BeautifulSoup
import MimeWriter
import requests
import urllib
import mysql.connector
import password
import sys
import csv
import smtplib
import os
import logging
import base64
import StringIO
import argparse

LINKSHARE = 2
PAIDONRESULTS = 9

def argument_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deeplink", help="manually setting the deeplink")
    parser.add_argument("--merchant_ids", help="merchant_IDs to test comma seperated")
    parser.add_argument("--status_id", help="manually setting the status_id, there must only be one")
    args = parser.parse_args()
    return args

def initLogging(level = logging.DEBUG):
    logging._levelNames[logging.CRITICAL]= '\033[1m\033[91mCRITICAL\033[0m'
    logging._levelNames[logging.ERROR]= '\033[91mERROR\033[0m'
    logging._levelNames[logging.WARNING]= '\033[93mWARNING\033[0m'
    logging._levelNames[logging.INFO]= '\033[94mINFO\033[0m'
    logging._levelNames[logging.DEBUG]= '\033[92mDEBUG\033[0m'

    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
    #handler.setFormatter(color.ColorFormatter("%(asctime)s %(levelname)s: %(message)s"))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(level)

def merchant_query(merchant_id):
    cnx = mysql.connector.connect(user=password.mysqluser, password=password.mysqlpassword, host=password.mysqlhost, database=password.mysqldatabase)
    cursor = cnx.cursor()
    cursor.execute("select md.id, md.merchant_id, md.domain, mm.network_deeplink, mm.skim_deeplink, mm.network_id, mm.status_id from mugic_merchants_domains md inner join mugic_merchant mm on mm.id = md.merchant_id where md.merchant_id = %s" , (merchant_id,))
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

def get_trackingurl(status_id,merchant_info):
    if status_id == '1001':
        tracking_url = merchant_info[0][3]
    elif status_id == '1002':
        tracking_url = merchant_info[0][4]
    else:
        tracking_url = None
    return tracking_url

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

def email_output():
    message = StringIO.StringIO()
    writer = MimeWriter.MimeWriter(message)
    writer.addheader("Subject", "Autotesting Link Generator")
    writer.startmultipartbody("mixed")
    part = writer.nextpart()
    body = part.startbody("text/plain")
    body.write("Hello,\n\nHere are your affliate links to send to the Turks.\n\nLove from the link generator bot. <3")
    part = writer.nextpart()
    part.addheader("Content-Transfer-Encoding", "base64")
    part.addheader("Content-disposition", "attachment;filename=links.csv")
    body = part.startbody("file/csv")
    base64.encode(open("links.csv", "rb"), body)
    writer.lastpart()
    fromaddr = 'amyerobinson27@gmail.com'
    toaddrs = 'autotesting@skimlinks.com'
    gmail_user = "%s" % (password.gmailuser)
    gmail_pwd = "%s" % (password.gmailpassword)
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(fromaddr, toaddrs, message.getvalue())
    server.quit()

if __name__ == '__main__':
    args = argument_parse()
    initLogging()
    merchant_ids = args.merchant_ids.split(',')
    with open('links.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(['merchant ID', 'domain', 'network ID', 'link', 'affiliate_link'])
        for merchant_id in merchant_ids:
            merchant_info = merchant_query(merchant_id)
            if not merchant_info:
                logging.error("Invalid Merchant ID %s", merchant_id)
            else:
                domain = merchant_info[0][2]
                status_id = str(merchant_info[0][6])
                network_id = merchant_info[0][5]
                logging.info(domain)
                if args.status_id:
                    status_id = str(args.status_id)
                if args.deeplink:
                    tracking_url = args.deeplink
                else:
                    logging.debug(status_id)
                    tracking_url = get_trackingurl(status_id,merchant_info)
                logging.debug(tracking_url)
                if tracking_url is None:
                    logging.error("Status_id outside range %s", status_id)
                    continue
                deeplinks = deeplink_extract(domain)
                logging.debug(deeplinks)
                if not deeplinks:
                    logging.error("No deeplinks obtained")
                    continue
                for link in deeplinks:
                    affiliate_link = create_affiliate_link(tracking_url, link, network_id)
                    logging.info(affiliate_link)
                    writer.writerow([merchant_id, domain, network_id, link, affiliate_link])
    email_output()
    print "All links obtained -- check your email."