import mysql.connector
import password

cnx = mysql.connector.connect(user=password.user, password=password.password, host=password.host, database=password.database)
cursor = cnx.cursor()
cursor.execute("select id, merchant_id, total_amount from mugic_comms order by id desc limit 5")
commissions = cursor.fetchall()
cursor.close()
cnx.close()
for commission in commissions:
    print commission

merchant_id = 1
cnx = mysql.connector.connect(user=password.user, password=password.password, host=password.host, database=password.database)
cursor = cnx.cursor()
cursor.execute(("select id, merchant_id, domain from mugic_merchants_domains where merchant_id = %s") % (merchant_id))
domain_list = cursor.fetchall()
cursor.close()
cnx.close()
for domain in domain_list:
    print domain