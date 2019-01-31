#! /usr/bin/env python3
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root"
)

cursor = mydb.cursor()
commande = ""
for line in open("doc/db/dboff_handmd.sql"):
    commande += line.replace('\n', ' ')
for cmd in commande.split(";"):
    cursor.execute(cmd)

"""
sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = [
  ('Peter', 'Lowstreet 4')]

mycursor.execute(sql, val)
mycursor.executemany(sql, val)

mydb.commit()

mycursor.lastrowid


sql = "UPDATE customers SET address = %s WHERE address = %s"
val = ("Valley 345", "Canyon 123")

mycursor.execute(sql, val)

mydb.commit()



mycursor.execute("SELECT * FROM customers")

myresult = mycursor.fetchall()

"""