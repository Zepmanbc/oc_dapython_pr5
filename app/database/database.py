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
    if 0, no limit, step of 200

    """

    QUANTITY_PRODUCTS = 200
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
        self.pagination_list = {
            "product": [],
            "substitute": [],
            "saved_substitute": []
        }
        # self.random_result = list()  # backup random list for pagination
        # self.substitute_proposition = list() # backup substitute proposition list for pagination
        # self.substitute_saved = list()  # backup substitute saved list pagination

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

    #########################
    #   CREATING DATABASE   #
    #########################

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
            toto = commande.split("--")
            for cmd in commande.split("--"):
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
        
        with open(self.STRUCTURE) as _file:
            category_list = json.load(_file)
        
        for category in category_list["category"]:
            sql = "INSERT INTO `Category` (`name`) VALUES (%s);"
            val = (category, )
            self.cursor.execute(sql, val)
            self.mydb.commit()
            category_id = self.cursor.lastrowid
            self._fill_with_off_data(category, category_id)
    
    def _fill_with_off_data(self, category, category_id):
        """Fill the DB with OFF data for each product type.

        Args:
            category (str): name of the category for the search
            category_id (int): store id of Category

        
        """
        print("Get \"{}\" items...".format(category))
        page = 1
        while True:
            _item = self._get_off_json(category, page)
            if _item["products"] == []: break
            qty_storing = (page - 1) * 200 + len(_item["products"])
            print("storing {}/{}...".format(qty_storing, _item["count"]))
            for info in _item["products"]:
                info = self._clean_info(info)
                sql = "INSERT INTO `Product` (`product_name`, \
                        `brands`, `quantity`, `stores`, `url`, `nutrition_grades`, `category_id`)\
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (
                    info["product_name"],
                    info["brands"],
                    info["quantity"],
                    info["stores"],
                    info["url"],
                    info["nutrition_grades_tags"][0],
                    category_id)
                self.cursor.execute(sql, val)
                self.mydb.commit()
            page += 1
            if qty_storing >= self.QUANTITY_PRODUCTS & self.QUANTITY_PRODUCTS != 0: break
        print("done")
    
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
        if info["nutrition_grades_tags"][0] not in ["a", "b", "c", "d", "e"]:
            info["nutrition_grades_tags"][0] = None

        return info
    
    def _get_off_json(self, item, page):
        """Get data from OFF API.

        default quantity return 200/page

        Args:
            item (str): name a product type
            page (int): page of result on OpenFoodFacts

        Return:
            json : list of product type
        
        """
        link = """https://fr.openfoodfacts.org/cgi/search.pl?action=process&search_terms={}
        &page_size=200&action=display&page={}&json=1""".format(item, page)
        return requests.get(link).json()

    #############
    #   QUERYS  #
    #############

    def get_category(self):
        """Get all the catégories.
        
        Returns:
            List ['category1', 'category2', ...]
        
        """
        self.cursor.execute("SELECT * FROM Category")
        return self.cursor.fetchall()

    @staticmethod
    def cut_nine_list(cut_list):
        """Convert a list in a list of list of 9 items.

        Args:
            cut_list (list): ex: [20 items]

        Return:
            list: ex:[[9 items], [9 items], [2 items]]

        """
        nine_list = list()
        while len(cut_list):
            nine_list.append(cut_list[:9])
            del(cut_list[:9])
        return nine_list

    def get_product(self, category_id):
        """Return list of 9 randomly product from a category.
        
        Args:

        Returns:

        """
        query ="""SELECT id, product_name, brands, quantity 
            FROM `Product` 
            WHERE Category_id={} 
            ORDER BY RAND()""".format(str(category_id))
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if len(result):
            self.pagination_list["product"] = self.cut_nine_list(result)
            return True
        else:
            return False
    
    def get_better_product(self, product_id):
        # query = "CALL get_better_product({})".format(product_id)
        # next(cursor.execute(query, multi=True))  # multi return an iterator
        # result = cursor.fetchall()

        # for toto in self.cursor.execute(query, multi=True):  # multi return an iterator
        #     result = self.cursor.fetchall()
        #     print(result)

        self.cursor.callproc("get_better_product", (product_id, ))
        # for buffer in self.cursor.stored_results():
        #     result = buffer.fetchall()
        result = next(self.cursor.stored_results()).fetchall()

        if len(result):
            self.pagination_list["substitute"] = self.cut_nine_list(result)
            return True
        else:
            return False

    def show_product_detail(self, origin_id, product_id):
        """Return product details.
        
        Args:

        Returns:

        """
        self.cursor.callproc("show_details", (origin_id, product_id))
        # for buffer in self.cursor.stored_results():
        #     result = buffer.fetchall()
        result = next(self.cursor.stored_results()).fetchall()
        # query = "CALL show_details ({}, {});".format(origin_id, product_id)
        # next(self.cursor.execute(query, multi=True))  # multi return an iterator
        # result = self.cursor.fetchall()

        # toto = self.cursor.callproc("show_details", (origin_id, product_id))
        # for toto in self.cursor.execute(query, multi=True):  # multi return an iterator
        #     print(toto.with_rows)
        #     print(toto.statement)




        if len(result):
            return result
        else:
            return False

    def show_substitute_detail(self, id_substitute):
        self.cursor.execute(
            "SELECT origin_id, substitute_id FROM V_Substitute WHERE id = {}".format(id_substitute)
            )
        return self.cursor.fetchall()

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

    def get_substitute_saved(self):
        """Return the view V_favorite.
        
        Returns:
            List [off_id, category_name, product_type, product_name, brands, quantity]
            False if SQL query return nothing.

        """
        self.cursor.execute("SELECT * FROM V_Substitute")
        result = self.cursor.fetchall()
        if len(result):
            self.pagination_list["saved_substitute"] = self.cut_nine_list(result)
            return True
        else:
            return False

if __name__ == "__main__":
    db = Database()

    """CREATE AND FILL IN"""
    # db.cursor.execute("DROP DATABASE IF EXISTS offdb;")
    # db.create_database()
    # db.fill_in_database()

    """TEST FUNCTIONS"""
    # print(db.get_product(1))
    # db.get_better_product(154)
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
    # print(db.show_substitute_detail(3))
    print(db.get_category())
    print(db.get_product(3))
    print(db.show_product_detail(12,45))
    print(db.get_better_product(33))
    print(db.show_product_detail(12,45))
    pass
