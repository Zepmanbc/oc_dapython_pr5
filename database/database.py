#! /usr/bin/env python3
"""Create offdb in MySQL and fill it with data from OpenFoodFacts."""

import mysql.connector
import json
import requests


class Database():
    """Create the Database.

    db = Database()
    db.create("data/dboff.sql")
    db.import_categories("data/categories.json")
    """

    def __init__(self):
        """Initialyse the connection."""
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="offdb"
        )
        self.cursor = self.mydb.cursor()

    def create(self, sql_file):
        """Read the SQL file and create the database and tables."""
        commande = ""
        for line in open(sql_file):
            commande += line.replace('\n', ' ')
        for cmd in commande.split(";"):
            self.cursor.execute(cmd)

    def import_categories(self,json_file):
        """Import the categories/products from the json and fill the db."""
        with open(json_file) as _f:
            categories = json.load(_f)
        
        for category in categories.keys():
            sql = "INSERT INTO `Category` (`name`) VALUES (%s);"
            val = (category, )
            self.cursor.execute(sql, val)
            self.mydb.commit()
            id_category = self.cursor.lastrowid

            for product in categories[category]:
                sql = "INSERT INTO `Product` (`name`, `category_id`) VALUES (%s, %s)"
                val = (product, id_category)
                self.cursor.execute(sql, val)
                self.mydb.commit()
                id_product = self.cursor.lastrowid
                self.fill_db(product, id_product)

    def fill_db(self, item, id_product):
        """Fill the DB with OFF data for each product type."""
        _item = self.get_json(item)
        if _item["count"] > 1000: _item["count"] = 1000
        print(item + " - " + str(_item["count"]))
        for info in _item["products"]:
            info = self.try_info(info)
            sql = "INSERT INTO `OffData` (`product_name`, \
                    `brands`, `quantity`, `stores`, `url`, `product_id`)\
                     VALUES (%s, %s, %s, %s, %s, %s)"
            val = (info["product_name"], info["brands"], info["quantity"], info["stores"], info["url"], id_product)
            # print(val)
            self.cursor.execute(sql, val)
            self.mydb.commit()
    
    @staticmethod
    def try_info(info):
        """Test OFF data if all fialds exists, or create missing fields."""
        for item in ["product_name", "brands", "quantity", "stores", "url"]:
            try:
                info[item]
            except:
                info[item] = ''
        return info
    
    @staticmethod
    def get_json(item):
        """Get data from OFF API."""
        link = """https://fr.openfoodfacts.org/cgi/search.pl?action=process&search_terms={}
        &additives=without&ingredients_from_palm_oil=without&ingredients_that_may_be_from_palm_oil=without&
        ingredients_from_or_that_may_be_from_palm_oil=without&sort_by=unique_scans_n&page_size=1000&
        axis_x=energy&axis_y=products_n&action=display&json=1""".format(item)
        return requests.get(link).json()


if __name__ == "__main__":
    db = Database()
    db.create("data/dboff.sql")
    db.import_categories("data/categories.json")

