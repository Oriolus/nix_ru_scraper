from mysql.connector import connection
from mysql.connector import errorcode
from mysql.connector import pooling

conn = connection.MySQLConnection(user='root', password='123qwe', host='127.0.0.1',database='nix_ru_scrap')
conn.connect()
cnx = conn.cursor()

query = ('select id, `url`, title from category')
cnx.execute(query)

for row in cnx.fetchall():
    print(row)

conn.close()
#