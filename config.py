"""Configuration file for Database.

QUANTITY_PRODUCTS : max numbers of Downloads from OpenfFoodFact per category, 0 is no limit

"""

dbconnect = {
    "QUANTITY_PRODUCTS" : 200,
    "HOST" : "localhost",
    "USER" : "root",
    "PASSWD" :"root",
    "DATABASE" : "offdb",
    "SQL_FILE" : "app/static/dboff.sql",
    "STRUCTURE" : "app/static/categories.json"
}