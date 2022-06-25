
import sqlite3

connection = sqlite3.connect('/home/flaxenink/mysite/clothes.db')

cursor = connection.cursor()

cursor.execute(''' CREATE TABLE IF NOT EXISTS qrclothes
(id INTEGER PRIMARY KEY AUTOINCREMENT, notes TEXT NOT NULL, userid TEXT NOT NULL, image TEXT) ''')

connection.commit()

cursor.execute(''' insert into qrclothes (id, notes, userid, image) values (1234567, 'blue jeans from gap size 32 waste', 'smiles@yahoo.com', NULL) ''' )
connection.commit()
connection.close()