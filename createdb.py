#! /usr/bin/env python3
"""Script for Database creation.
Force to remove database"""

from app.database.database import Database
import config
db = Database(config.dbconnect)

"""CREATE AND FILL IN"""
db.cursor = db.mydb.cursor()
db.cursor.execute("DROP DATABASE IF EXISTS {};".format(config.dbconnect["DATABASE"]))
db.cursor.close()
db.create_database()
db.fill_in_database()