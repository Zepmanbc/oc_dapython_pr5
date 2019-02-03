#! /usr/bin/env python3
"""Interface for Pure Beurre."""

import sys
import os
# from ..database.database import Database
sys.path.append('app/')
from database.database import Database

class Gui():
    def __init__(self):
        self.db = Database()
        try:
            self.db.cursor
        except:
            self.clear()
            print("Création de la base...")
            self.db.create_database()
            print("Récupération des données en cours...")
            self.db.fill_in_database()
    
    def screen_intro(self):
        while True:
            self.clear()
            print("""
            1 - Quel aliment souhaitez-vous remplacer ? 
            2 - Retrouver mes aliments substitués.

            0 - Quitter
            """)
            answer = input("Votre choix : ")
            try:
                answer = int(answer)
                if answer in range(3):
                    return answer
            except:
                pass

    def screen_category(self):
        list_category = self.db.get_category()
        while True:
            self.clear()
            for category in list_category:
                print("{} - {}".format(category[0],category[1]))
            print("\n0 - retour")
            answer = input("\nVotre choix : ")

            try:
                answer = int(answer)
                if answer in range(6):
                    return answer
            except:
                pass

    def screen_type_product(self, category_id):
        list_type_product = self.db.get_type_product(category_id)
        while True:
            self.clear()
            number = 0
            for type_product in list_type_product:
                number += 1
                print("{} - {} - (id:{})".format(number, type_product[1], type_product[0]))
            print("\n0 - retour")
            answer = input("\nVotre choix : ")
            
            try:
                answer = int(answer)
                if answer in range(len(list_type_product) + 1):
                    if answer == 0: return 0
                    return list_type_product[answer - 1][0]
            except:
                pass

    def screen_product(self, product_id):
        list_product = self.db.get_product(product_id)
        while True:
            self.clear()
            number = 0
            for product in list_product:
                number += 1
                id = product[0]
                name = product[1]
                brand = product[2]
                qty = product[3]
                print("{} - {} - {} - {} (id:{})".format(number, name, brand, qty, id ))
            print("\n0 - retour")
            answer = input("\nVotre choix : ")
            
            try:
                answer = int(answer)
                if answer in range(len(list_product) + 1):
                    if answer == 0: return 0
                    return list_product[answer - 1][0]
            except:
                pass

    def screen_show_product(self, id_off):
        detail = self.db.show_product(id_off)
        while True:
            self.clear()
            number = 0
            for product in detail:

                id = product[0]
                name = product[1]
                brand = product[2]
                qty = product[3]
                store = product[4]
                url = product[5]
                fav = product[6]
                if fav:
                    print("*** PRESENT DANS LES FAVORIS ***\n")

                print("Nom              : {}".format(name))
                print("Marque           : {}".format(brand))
                print("Conditionnement  : {}".format(qty))
                print("Magasins         : {}".format(store))
                print("Lien OFF         : {}".format(url))
                
            if fav:
                print("\n1 - Supprimer des Favoris")
            else:
                print("\n1 - Enregistrer dans les Favoris")
            print("0 - retour")
            answer = input("\nVotre choix : ")
            
            try:
                answer = int(answer)
                if answer in range(2):
                    if answer:
                        self.db.set_favorite(id)
                    return answer
            except:
                pass

    def screen_show_favorite(self):
        list_product = self.db.get_favorites()
        if list_product:
            while True:
                self.clear()
                number = 0
                for product in list_product:
                    number += 1
                    print("{} - {}".format(number, product))
                
                print("\n0 - retour")
                answer = input("\nVotre choix : ")
                
                try:
                    answer = int(answer)
                    if answer in range(len(list_product) + 1):
                        if answer == 0: return 0
                        return list_product[answer - 1][0]
                except:
                    pass
        else:
            self.clear()
            print("*** PAS DE FAVORIS ***")
            input("appuyez sur une touche...")
    
    @staticmethod
    def clear():
        if os.uname()[0] == "Windows":
            os.system('cls')
        else:
            os.system('clear')

if __name__ == "__main__":
    gui = Gui()
    # gui.screen_intro()
    # cat = gui.screen_category()
    # if cat:
    #     prod = gui.screen_type_product(cat)
    #     if prod:
    #         print(gui.screen_product(prod))
    # while gui.screen_show_product(5):
    #     pass
    gui.screen_show_favorite()
    pass
