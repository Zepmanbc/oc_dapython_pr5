#! /usr/bin/env python3
import requests
# import json

products = {
    "petit dejeuner" : ["brioche", "pate a tartiner", "jus de fruit", "Chocolats en poudre"], 
    "dejeuner" : ["sandwich", "salade", "taboulé", "crudité", "fromage"], 
    "gouter": ["biscuits", "compotes"], 
    "diner" : ["pizza", "gratin", "choucroute", "ravioli"], 
    "dessert" : ["creme chocolat", "glaces", "patisserie", "yaourt aux fruits"]
}

def get_json(item):
    link = """https://fr.openfoodfacts.org/cgi/search.pl?action=process&search_terms={}
    &additives=without&ingredients_from_palm_oil=without&ingredients_that_may_be_from_palm_oil=without&
    ingredients_from_or_that_may_be_from_palm_oil=without&sort_by=unique_scans_n&page_size=20&
    axis_x=energy&axis_y=products_n&action=display&json=1""".format(item)
    return requests.get(link).json()

def print_first(item):
    _item = get_json(item)
    first = _item["products"][0]
    print(first["product_name"])
    print(first["brands"])
    print(first["quantity"])
    print(first["stores"])
    print(first["url"])

for category in products.keys():
    food = products[category]
    for item in food:
        print_first(item)
