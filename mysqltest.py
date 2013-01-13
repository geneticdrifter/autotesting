import mysql.connector
import password

#if __name__ == '__main__':
    #cnx = mysql.connector.connect(user=password.user, password=password.password, host=password.host, database=password.database)
    #cursor = cnx.cursor()
    #cursor.execute("select id, merchant_id, total_amount from mugic_comms order by id desc limit 5")
    #commissions = cursor.fetchall()
    #cursor.close()
    #cnx.close()
    #print rows
    #for commission in commissions:
    #    print commission

if __name__ == '__main__':        
    cnx = mysql.connector.connect(user=password.user, password=password.password, host=password.host, database=password.database)
    cursor = cnx.cursor()
    cursor.execute("select * from mugic_merchants_domains where merchant_id = 1")
    domain_list = cursor.fetchall()
    cursor.close()
    cnx.close()
    for domain in domain_list:
        print domain