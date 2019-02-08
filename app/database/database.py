#! /usr/bin/env python3
"""Create offdb in MySQL and fill it with data from OpenFoodFacts."""

import mysql.connector
import json
import requests

class Database():
    """Create the Database.

    Set for a MySQL Database.

    Change global variables to set connection configuration (HOST, USER, PASSWD)

    initialyse the database with:
        db = Database()
        db.create() => read SQL_FILE to create the database, tables, and a view
        db.import_categories() => read STRUCTURE to fill in TABLES and ask OpenFoodFacts

    change QUANTITY_PRODUCTS to set max product recorded for a product_type

    """

    QUANTITY_PRODUCTS = 50
    HOST = "localhost"
    USER = "root"
    PASSWD ="root"
    DATABASE = "offdb"
    SQL_FILE = "app/static/dboff.sql"
    STRUCTURE = "app/static/categories.json"

    def __init__(self):
        """Initialyse the connection.
        
        If connection is ok, create th cursor
        Else return None
        
        """
        self.random_result = list()

        if self.create_connection():
            self.cursor = self.mydb.cursor()
        else:
            self.mydb = False

    def create_connection(self):
        """Test MySQL connection.
        
        Return:
            Boolean
            console print OK or error message.

        """
        try:
            self.mydb = mysql.connector.connect(
                host=self.HOST,
                user=self.USER,
                passwd=self.PASSWD,
                database=self.DATABASE
            )
            print("Connection OK")
            return True
        except mysql.connector.Error as err:
            print(err)
            return False

    def create_database(self):
        """Read the SQL file and create the database and tables.
        
        SQL_FILE (str): path to a sql file command.

        Creates DATABASE, TABLES, VIEW
        
        """
        try:
            self.mydb = mysql.connector.connect(
                host=self.HOST,
                user=self.USER,
                passwd=self.PASSWD,
            )
            print("Connection OK")
        except mysql.connector.Error as err:
            print(err)
            return False

        self.cursor = self.mydb.cursor()
        commande = ""
        try:
            for line in open(self.SQL_FILE):
                commande += line.replace('\n', ' ')
        except FileNotFoundError:
            print("File not Found: {}".format(self.SQL_FILE))
        try:
            for cmd in commande.split(";"):
                self.cursor.execute(cmd)
        except mysql.connector.Error as err:
            print(err)
        
    def fill_in_database(self):
        """Import the categories/products from the json and fill the db.
        
        STRUCTURE (str): path to a json file
            {category:[product_type1, ... ], ... }

        """
        try:
            self.cursor
        except AttributeError:
            print("Need to create offdb")
            return None
        
        with open(self.STRUCTURE) as _f:
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
                self._fill_with_off_data(product, id_product)

    def _fill_with_off_data(self, item, id_product):
        """Fill the DB with OFF data for each product type.
        
        Fill in the OffData TABLE.

        Args:
            item (dict): json data from one product OpenFoodFacts
            id_product (int): Product type id
        
        """
        _item = self._get_off_json(item)
        if _item["count"] > self.QUANTITY_PRODUCTS: _item["count"] = self.QUANTITY_PRODUCTS
        print(item + " - " + str(_item["count"]))
        for info in _item["products"]:
            info = self._clean_info(info)
            sql = "INSERT INTO `OffData` (`product_name`, \
                    `brands`, `quantity`, `stores`, `url`, `nutrition_grades`, `product_id`)\
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (
                info["product_name"],
                info["brands"],
                info["quantity"],
                info["stores"],
                info["url"],
                info["nutrition_grades_tags"][0],
                id_product)
            self.cursor.execute(sql, val)
            self.mydb.commit()
    
    @staticmethod
    def _clean_info(info):
        r"""Test OFF data if all fields exists, or create missing fields.

        Also replace \n with _
        
        Args:
            info (dict): one product data from OpenFoodFacts

        Returns:
            dict : with these keys "product_name", "brands", "quantity", "stores", "url"

        """
        for item in ["product_name", "brands", "quantity", "stores", "url"]:
            try:
                info[item]
            except:
                info[item] = ''
            # Clean data
            info[item] = info[item].replace('\n', '_')
        if info["nutrition_grades_tags"][0] in ["unknown", "not-applicable"]:
            info["nutrition_grades_tags"][0] = ""

        return info
    
    def _get_off_json(self, item):
        """Get data from OFF API.
        
        QUANTITY_PRODUCTS (int) sets the max results.

        Args:
            item (str): name a product type

        Return:
            json : list of product type
        
        """
        link = """https://fr.openfoodfacts.org/cgi/search.pl?action=process&search_terms={}
        &page_size={}&action=display&json=1""".format(item, self.QUANTITY_PRODUCTS)
        return requests.get(link).json()

    def get_category(self):
        """Get all the catégories.
        
        Returns:
            List ['category1', 'category2', ...]
        
        """
        self.cursor.execute("SELECT * FROM Category")
        return self.cursor.fetchall()

    def get_type_product(self, category_id):
        """Get all product types from a category.
        
        Args:
            category_id (int): Category id

        Returns:
            List ['product_type1', 'product_type2', ...]
            False if SQL query return nothing.
        
        """
        self.cursor.execute("SELECT * FROM Product WHERE category_id={}".format(str(category_id)))
        result = self.cursor.fetchall()
        if len(result):
            return result
        else:
            return False

    def get_product(self, product_id):
        """Return 9 random product from a product type.
        
        Args:

        Returns:

        """
        self.cursor.execute(
            """SELECT id, product_name, brands, quantity 
            FROM `OffData` 
            WHERE product_id={} 
            ORDER BY RAND()""".format(str(product_id)))
        result = self.cursor.fetchall()
        if len(result):
            self.random_result = result
            return True
        else:
            return False

    def show_product(self, off_id):
        """Return product details.
        
        Args:
            off_id (int): OffData id

        Returns:
            List [id, product_name, brands, quantity, stores, url, nutrition_grades, product_id]
            False if SQL query return nothing.

        """
        self.cursor.execute("SELECT * FROM `OffData` WHERE id={}".format(str(off_id)))
        result = self.cursor.fetchall()
        if len(result):
            return result
        else:
            return False

    def show_better_product(self, product_id, grade, offset=0):
        if not grade: grade = 'z'
        self.cursor.execute("""SELECT * FROM `OffData` 
            WHERE product_id={}
            AND `nutrition_grades` <= '{}'
            AND `nutrition_grades` <> ''
            ORDER BY `nutrition_grades`
            LIMIT 9 OFFSET {}""".format(product_id, grade, offset))
        result = self.cursor.fetchall()
        if len(result):
            return result
        else:
            return False

    def set_substitute(self, origin_id, substitute_id):
        self.cursor.execute(
            """INSERT INTO `Substitute` 
            (`origin_id`, `substitute_id`) 
            VALUES 
            ('{}', '{}');""".format(origin_id, substitute_id))
        self.mydb.commit()

    def delete_substitute(self, id):
        self.cursor.execute(("DELETE FROM `Substitute` WHERE `id` = {}").format(id))
        self.mydb.commit()

    def get_substitute(self):
        """Return the view V_favorite.
        
        Returns:
            List [off_id, category_name, product_type, product_name, brands, quantity]
            False if SQL query return nothing.

        """
        self.cursor.execute("SELECT * FROM V_Substitute")
        result = self.cursor.fetchall()
        if len(result):
            return result
        else:
            return False

if __name__ == "__main__":
    db = Database()
    # db.cursor.execute("DROP DATABASE IF EXISTS offdb;")
    # db.create_database()
    # db.fill_in_database()
    # db.get_category()
    # print(db.get_type_product(4))
    # print(db.get_product(4,5))
    # print(db.show_better_product(4,''))
    # print(db.show_product(64))
    # db.set_favorite(5)
    # print(db.get_favorites())
    # db.set_substitute(3,6)
    # db.set_substitute(35,65)
    # db.set_substitute(33,64)
    # db.set_substitute(37,67)
    db.delete_substitute(2)
    pass
