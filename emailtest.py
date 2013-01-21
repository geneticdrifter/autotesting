import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import password

msg['Subject'] = "Merchant links for auto testing"
msg['From'] = str(password.gmailuser)
msg['To'] = "autotesting@skimlinks.com"

text = "Greetings Human,/n/nHere are your links to send to the Turks./n/nLove from the merchant link generator bot. <3"