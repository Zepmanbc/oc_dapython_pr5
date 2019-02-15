#! /usr/bin/env python3
"""Create offdb in MySQL and fill it with data from OpenFoodFacts."""

import json
import mysql.connector
import requests


class Database():
    """Create the Database.

    Set for a MySQL Database.

    Change config.py to set connection configuration
    (HOST, USER, PASSWD, DATABASE)

    initialyse the database with:
        db = database(configuration_dict)
        db.create() => read SQL_FLES to create the DATABASE, TABLES, VIEW and PROCEDURES
        db.fill_in_database() => read structure to fill in TABLES
                                and ask OpenFoodFacts

    change quantity_products to set max product recorded for a product_type
    if 0, no limit, step of 200

    """

    def __init__(self, DBCONNECT):
        """Initialyse the connection.

        Args:
            DBCONNECT (dict): configuration
                default:
                    {
                        "QUANTITY_PRODUCTS" : 200,
                        "HOST" : "localhost",
                        "USER" : "root",
                        "PASSWD" :"root",
                        "DATABASE" : "offdb",
                        "SQL_FILE" : "app/static/dboff.sql",
                        "STRUCTURE" : "app/static/categories.json"
                    }

        If connection is not ok, set mydb to False
        """
        self.dbconnect = DBCONNECT

        self.pagination_list = {
            "product": [],
            "substitute": [],
            "saved_substitute": []
        }

        if not self.create_connection():
            self.mydb = False
        else:
            self.cursor = self.mydb.cursor()  # just for init the variable in __init__
            self.cursor.close()

    def create_connection(self):
        """Test MySQL connection.

        Return:
            Boolean
            console print OK or error message.

        """
        try:
            self.mydb = mysql.connector.connect(
                host=self.dbconnect["HOST"],
                user=self.dbconnect["USER"],
                passwd=self.dbconnect["PASSWD"],
                database=self.dbconnect["DATABASE"]
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

        sql_file (str): path to a sql file command.

        Creates DATABASE, TABLES, VIEW, PROCEDURE.
        Only the structure.

        """
        try:
            self.mydb = mysql.connector.connect(
                host=self.dbconnect["HOST"],
                user=self.dbconnect["USER"],
                passwd=self.dbconnect["PASSWD"],
            )
            print("Connection OK")
        except mysql.connector.Error as err:
            print(err)
            return False

        self.cursor = self.mydb.cursor()
        commande = ""
        try:
            for line in open(self.dbconnect["SQL_FILE"]):
                commande += line.replace('\n', ' ')
        except FileNotFoundError:
            print("File not Found: {}".format(self.dbconnect["SQL_FILE"]))
        try:
            for cmd in commande.split("--"):
                self.cursor.execute(cmd)
        except mysql.connector.Error as err:
            print(err)
        self.cursor.close()
        return True

    def fill_in_database(self):
        """Import the categories/products from the json and fill the db.

        structure (str): path to a json file
            {category:[product_type1, ... ], ... }

        """
        try:
            self.cursor = self.mydb.cursor()
        except AttributeError:
            print("Need to create offdb")
            return None

        with open(self.dbconnect["STRUCTURE"]) as _file:
            category_list = json.load(_file)

        for category in category_list["category"]:
            sql = "INSERT INTO `Category` (`name`) VALUES (%s);"
            val = (category, )
            self.cursor.execute(sql, val)
            self.mydb.commit()
            category_id = self.cursor.lastrowid
            self._fill_with_off_data(category, category_id)
        self.cursor.close()
        return True

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
            if _item["products"] == []:
                break
            qty_storing = (page - 1) * 200 + len(_item["products"])
            print("storing {}/{}...".format(qty_storing, _item["count"]))
            for info in _item["products"]:
                info = self._clean_info(info)
                sql = "INSERT INTO `Product` (`product_name`, \
                        `brands`, `quantity`, `stores`, `url`, \
                            `nutrition_grades`, `category_id`)\
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
            if qty_storing >= self.dbconnect["QUANTITY_PRODUCTS"] & self.dbconnect["QUANTITY_PRODUCTS"] != 0:
                break
        print("done")

    @staticmethod
    def _clean_info(info):
        r"""Test OFF data if all fields exists, or create missing fields.

        Also replace \n with _

        Args:
            info (dict): one product data from OpenFoodFacts

        Returns:
            dict : with these keys
                    "product_name",
                    "brands",
                    "quantity",
                    "stores",
                    "url"

        """
        for item in ["product_name", "brands", "quantity", "stores", "url"]:
            if item not in info.keys():
                info[item] = ''
            # try:
            #     info[item]
            # except:
            #     info[item] = ''
            # Clean data
            info[item] = info[item].replace('\n', '_')
        if info["nutrition_grades_tags"][0] not in ["a", "b", "c", "d", "e"]:
            info["nutrition_grades_tags"][0] = None

        return info

    @staticmethod
    def _get_off_json(item, page):
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
        self.cursor = self.mydb.cursor()
        self.cursor.execute("SELECT * FROM Category")
        resutl = self.cursor.fetchall()
        self.cursor.close()
        return resutl

    @staticmethod
    def cut_nine_list(cut_list):
        """Convert a list in a list of list of 9 items.

        Args:
            cut_list (list): ex: [20 items]

        Return:
            list: ex:[[9 items], [9 items], [2 items]]

        """
        nine_list = list()
        while cut_list:
            nine_list.append(cut_list[:9])
            del cut_list[:9]
        return nine_list

    def get_product(self, category_id):
        """Return a list of 9 randomly products list from a category.

        Args:
            category_id (int): id from Category TABLE

        Returns:
            list:
            [
                [
                    [id, designation]
                    ...
                    [id, designation]
                ]
                [ 9 Products List ]
                [ 9 Products List ]
                ...
            ]

        """
        self.cursor = self.mydb.cursor()
        query = """SELECT id,
            CONCAT(
                UPPER(IFNULL(nutrition_grades, "X")), " : ",
                product_name, " ",
                brands, " ",
                quantity
            ) as product
            FROM `Product`
            WHERE Category_id={}
            ORDER BY RAND()""".format(str(category_id))
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.cursor.close()
        if result:
            self.pagination_list["product"] = self.cut_nine_list(result)
            return True
        return False

    def get_better_product(self, product_id):
        """Return a list of substitutes for a product.

        Return a list of 9 products list from the same category,
        with at least the same nutrition grade
        ordered by nutrition grade (A>B>C>D)
        does not return nutrition grade less products

        Args:
            product_id (int): id of origin product.

        Returns:
            list:
            [
                [
                    [id, designation]
                    ...
                    [id, designation]
                ]
                [ 9 Products List ]
                [ 9 Products List ]
                ...
            ]

        """
        self.cursor = self.mydb.cursor()
        self.cursor.callproc("get_better_product", (product_id, ))
        result = next(self.cursor.stored_results()).fetchall()
        self.cursor.close()
        if result:
            self.pagination_list["substitute"] = self.cut_nine_list(result)
            return True
        return False

    def show_product_detail(self, origin_id, substitute_id):
        """Return product details.

        Call PROCEDURE show_details

        Args:
            origin_id (int): id fron origin product
            substitute_id (int): id from substitute product

        Returns:
            list:[
                    origin_designation
                    origin_grade
                    substitute_designation
                    substitute_grade
                    url
                    stores
                    substitute_exist : return id od Substitute TABLE or NULL
                ]

        """
        self.cursor = self.mydb.cursor()
        self.cursor.callproc("show_details", (origin_id, substitute_id))
        result = next(self.cursor.stored_results()).fetchall()
        self.cursor.close()
        if result:
            return result
        return False

    def set_substitute(self, origin_id, substitute_id):
        """Save a combinaison of 2 products Origin and Substitute.

        INSERT in Substitute TABLE

        Args:
            origin_id (int): id fron origin product
            substitute_id (int): id fron substitute product

        """
        self.cursor = self.mydb.cursor()
        self.cursor.execute(
            """INSERT INTO Substitute
            (origin_id, substitute_id)
            VALUES
            ('{}', '{}');""".format(origin_id, substitute_id))
        self.cursor.close()
        self.mydb.commit()

    def delete_substitute(self, substitute_id):
        """Delete a combinaison of Origin and Substitute product.

        DELETE data on Substitute TABLE

        Args:
            substitute_id (int): id of Substitute TABLE

        """
        self.cursor = self.mydb.cursor()
        self.cursor.execute(("DELETE FROM Substitute WHERE id = {}").format(substitute_id))
        self.cursor.close()
        self.mydb.commit()

    def get_substitute_saved(self):
        """Return the view V_favorite.

        Returns:
            List [
                id,
                products, => full designation
                        (category,
                        nutrition grades,
                        origin and substitute product)
                origin_id,
                substitute_id
                ]
            False if SQL query return nothing.

        """
        self.cursor = self.mydb.cursor()
        self.cursor.execute("SELECT * FROM V_Substitute")
        result = self.cursor.fetchall()
        self.cursor.close()
        if result:
            self.pagination_list["saved_substitute"] = self.cut_nine_list(result)
            return True
        return False


if __name__ == "__main__":
    import sys
    sys.path.append('.')
    # import config
    # db = Database(config.DBCONNECT)

    # """CREATE AND FILL IN"""
    # db.cursor = db.mydb.cursor()
    # db.cursor.execute("DROP DATABASE IF EXISTS offdb;")
    # db.create_database()
    # db.fill_in_database()

    # """TEST FUNCTIONS"""
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
    # print(db.get_category())
    # print(db.get_product(3))
    # print(db.show_product_detail(12,45))
    # print(db.get_better_product(33))
    # print(db.show_product_detail(12,45))
    # print(db.get_substitute_saved())
