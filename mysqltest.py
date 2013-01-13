import mysql.connector
import password

if __name__ == '__main__':
    cnx = mysql.connector.connect(user=password.user, password=password.password, host=password.host, database=password.database)
    cursor = cnx.cursor()
    cursor.execute("select id, merchant_id, total_amount from mugic_comms order by id desc limit 5")
    commissions = cursor.fetchall()
    cursor.close()
    cnx.close()
    #print rows
    for commission in commissions:
        print commission