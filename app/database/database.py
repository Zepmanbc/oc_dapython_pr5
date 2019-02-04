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
        if self.create_connection():
            self.cursor = self.mydb.cursor()
        else:
            return None

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
            info = self._try_off_info(info)
            sql = "INSERT INTO `OffData` (`product_name`, \
                    `brands`, `quantity`, `stores`, `url`, `product_id`)\
                     VALUES (%s, %s, %s, %s, %s, %s)"
            val = (info["product_name"], info["brands"], info["quantity"], info["stores"], info["url"], id_product)
            self.cursor.execute(sql, val)
            self.mydb.commit()
    
    @staticmethod
    def _try_off_info(info):
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
        &additives=without&ingredients_from_palm_oil=without&ingredients_that_may_be_from_palm_oil=without&
        ingredients_from_or_that_may_be_from_palm_oil=without&sort_by=unique_scans_n&page_size={}&
        axis_x=energy&axis_y=products_n&action=display&json=1""".format(item, self.QUANTITY_PRODUCTS)
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
            product_id (int): product_type id

        Returns:
            Dict {[id, product_name, brands, quantity], ...}
            False if SQL query return nothing.

        """
        self.cursor.execute("SELECT id, product_name, brands, quantity FROM `OffData` WHERE product_id={} ORDER BY RAND() LIMIT 9".format(str(product_id)))
        result = self.cursor.fetchall()
        if len(result):
            return result
        else:
            return False

    def show_product(self, off_id):
        """Return product details.
        
        Args:
            off_id (int): OffData id

        Returns:
            List [id, product_name, brands, quantity, stores, url, user_favorite, product_id]
            False if SQL query return nothing.

        """
        self.cursor.execute("SELECT * FROM `OffData` WHERE id={}".format(str(off_id)))
        result = self.cursor.fetchall()
        if len(result):
            return result
        else:
            return False

    def set_favorite(self, off_id):
        """Switch the favorite flag for a product.
        
        Switch `user_favorite` to 0 or 1depending the previous value.

        Args:
            off_id (int): OffData id
        
        """
        self.cursor.execute("SELECT user_favorite FROM `OffData` WHERE id={}".format(str(off_id)))
        result = self.cursor.fetchone()[0]
        if result:
            self.cursor.execute("UPDATE OffData SET user_favorite = 0 WHERE id = {};".format(str(off_id)))
        else:
            self.cursor.execute("UPDATE OffData SET user_favorite = 1 WHERE id = {};".format(str(off_id)))
        self.mydb.commit()

    def get_favorites(self):
        """Return the view V_favorite.
        
        Returns:
            List [off_id, category_name, product_type, product_name, brands, quantity]
            False if SQL query return nothing.

        """
        self.cursor.execute("SELECT * FROM V_favorite")
        result = self.cursor.fetchall()
        if len(result):
            return result
        else:
            return False

if __name__ == "__main__":
    db = Database()
    # db.create_database("app/static/dboff.sql")
    # db.fill_in_database("app/static/categories.json")
    # db.get_category()
    # print(db.get_type_product(4))
    # print(db.get_product(4))
    # print(db.show_product(64))
    # db.set_favorite(5)
    # print(db.get_favorites())
    pass
