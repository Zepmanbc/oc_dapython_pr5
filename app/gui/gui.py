#! /usr/bin/env python3
"""Interface for Pure Beurre."""

import sys
import os

sys.path.append('app/')
from database.database import Database

class Gui():
    """Generate all the screens to navigate throught Pur Beurre software.

    initialize the object, the Database will be initialised too
    gui = Gui()

    if gui.db:  # test if connection is OK
        while len(gui.current_screen):  # loop while there is a screen to show
            gui.screen_select()

    gui.current_screen = [(screen_name, arg), (screen_name, arg)]
    screen_name (str): method name for wanted screen
    arg (int): arg for screen method, some screen don't have arg
    to go back: gui.current_screen.pop()

    gui.screen_select() shows the last screen in gui.current_screen list

    """

    def __init__(self):
        """Initialise the Database and print intro screen.

        If Database doesn't exist, create and fill it.
        """
        self.screen_config = {
            "screen_intro": self.screen_intro,
            "screen_select_category": self.screen_select_category,
            "screen_select_product": self.screen_select_product,
            "screen_select_substitute": self.screen_select_substitute,
            "screen_detail_substitute": self.screen_detail_substitute,
            "screen_show_substitute": self.screen_show_substitute
        }

        self.db = Database()
        if self.db.mydb:
            try:
                self.db.cursor
            except:
                self.clear()
                print("Création de la base...")
                self.db.create_database()
                print("Récupération des données en cours...")
                self.db.fill_in_database()
            self.current_screen = [("screen_intro",)]
        else:
            pass
            # self.db = False
    
    def screen_select(self):
        """Display the last screen in current_screen.
        
        screen item is a Tuple
        ("screen_name", *args)
        """
        screen = self.current_screen[-1]
        self.screen_config[screen[0]](*screen[1:])

    def screen_intro(self):
        """Print the intro screen."""
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
                if answer == 1:
                    self.current_screen.append(("screen_select_category",))
                elif answer == 2:
                    self.current_screen.append(("screen_show_substitute",))
                elif answer == 0:
                    self.current_screen.pop()
                break
            except:
                pass

    def screen_select_category(self):
        print("screen_select_category")
        pass

    def screen_select_product(self, category_id, page=0):
        print("screen_select_product")
        pass

    def screen_select_substitute(self, category_id, nutrition_grade, page=0):
        print("screen_select_substitute")
        pass

    def screen_detail_substitute(self, origin_id, subtitute_id):
        print("screen_detail_substitute")
        pass

    def screen_show_substitute(self):
        print("screen_show_substitute")
        pass


    # def screen_category(self):
    #     """Print category list.

    #     From Category TABLE.

    #     """
    #     list_category = self.db.get_category()
    #     while True:
    #         self.clear()
    #         for category in list_category:
    #             print("{} - {}".format(category[0],category[1]))
    #         print("\n0 - retour")
    #         answer = input("\nVotre choix : ")

    #         try:
    #             answer = int(answer)
    #             if answer in range(len(list_category) + 1):
    #                 if answer == 0:
    #                     self.current_screen.pop()
    #                 else:
    #                     self.current_screen.append(("screen_type_product", answer))
    #                 break
    #         except:
    #             pass

    # def screen_product(self, category_id, page=0):
    #     """Print list of product type for a category.

    #     Args:
    #         category_id (int): if from Category TABLE.
    #     """
    #     list_type_product = self.db.get_type_product(category_id)
    #     while True:
    #         self.clear()
    #         number = 0
    #         for type_product in list_type_product:
    #             number += 1
    #             print("{} - {}".format(number, type_product[1]))
    #         print("\n0 - retour")
    #         answer = input("\nVotre choix : ")
            
    #         try:
    #             answer = int(answer)
    #             if answer in range(len(list_type_product) + 1):
    #                 if answer == 0:
    #                     self.current_screen.pop()
    #                 else:
    #                     self.current_screen.append(("screen_product", list_type_product[answer - 1][0]))
    #                 break
    #         except:
    #             pass

    # # def screen_product(self, product_id):
    #     """Print list of 9 products.

    #     Args:
    #         product_id (int): id of a product type from Product TABLE.

    #     """
    #     list_product = self.db.get_product(product_id)
    #     while True:
    #         self.clear()
    #         number = 0
    #         for product in list_product:
    #             number += 1
    #             # id = product[0]
    #             name = product[1]
    #             brand = product[2]
    #             qty = product[3]
    #             print("{} - {} - {} - {}".format(number, name, brand, qty))
    #         print("\n0 - retour")
    #         answer = input("\nVotre choix : ")
            
    #         try:
    #             answer = int(answer)
    #             if answer in range(len(list_product) + 1):
    #                 if answer == 0:
    #                     self.current_screen.pop()
    #                     self.db.random_result = None
    #                 else:
    #                     self.current_screen.append(("screen_show_product", list_product[answer - 1][0]))
    #                 break
    #         except:
    #             pass

    # def screen_show_product(self, id_off):
    #     """Print detail of a product.

    #     Args:
    #         id_off (int): id of a product from offData TABLE.

    #     """
    #     detail = self.db.show_product(id_off)
    #     while True:
    #         self.clear()
    #         number = 0
    #         for product in detail:

    #             id = product[0]
    #             name = product[1]
    #             brand = product[2]
    #             qty = product[3]
    #             store = product[4]
    #             url = product[5]
    #             grade = product[6]
    #             type_product = product[7]

    #             print("Nom              : {}".format(name))
    #             print("Marque           : {}".format(brand))
    #             print("Conditionnement  : {}".format(qty))
    #             print("Magasins         : {}".format(store))
    #             print("Lien OFF         : {}".format(url))
                
    #         print("\n1 - Sélectionner un substitut")
    #         print("0 - retour")
    #         answer = input("\nVotre choix : ")
            
    #         try:
    #             answer = int(answer)
    #             if answer in range(2):
    #                 if answer:
    #                     search = (type_product, grade)
    #                     self.current_screen.append(("screen_show_substitute", search))
    #                     # self.db.show_better_products(id)
    #                 else:
    #                     self.current_screen.pop()
    #                 break
    #         except:
    #             pass

    # def screen_show_better_product(self, search):
    #     (product_id, grade) = search
    #     list_substitute = self.db.show_better_product(product_id, grade)
    #     for product in list_substitute:
    #         print(product)

    # def screen_show_substitute(self):
    #     """Print favorites."""
    #     list_product = self.db.get_substitute()
    #     if list_product:
    #         while True:
    #             self.clear()
    #             number = 0
    #             for product in list_product:
    #                 number += 1
    #                 id = product[0]
    #                 category = product[1]
    #                 product_type = product[2]
    #                 origin_id = product[3]
    #                 origin_designation = product[4]
    #                 substitude_id = product[5]
    #                 substitute_designation = product[6]
    #                 product_name = "{} - {} - {}".format(product[3], product[4], product[5])
    #                 row = category + product_type + origin_designation + substitute_designation
    #                 print("{} - {}".format(number, row))
                
    #             print("\n0 - retour")
    #             answer = input("\nVotre choix : ")
                
    #             try:
    #                 answer = int(answer)
    #                 if answer in range(len(list_product) + 1):
    #                     if answer == 0:
    #                         self.current_screen.pop()
    #                     else:
    #                         self.current_screen.append(("screen_show_product", list_product[answer - 1][0]))
    #                     break
    #             except:
    #                 pass
    #     else:
    #         self.clear()
    #         print("*** PAS DE SUBSTITUT ***")
    #         input("appuyez sur une touche...")
    
    # def show_substitude_detail(self, id_Substitute):
    #     [(origin_id, substitute_id)] = self.db.show_substitute_detail(id_Substitute)
    #     origin_detail = self.db.show_product(origin_id)
    #     substitute_detail = self.db.show_product(substitute_id)
    #     while True:
    #         self.clear()
    #         message_list = ["Produit de substitution", "Produit d'origine"]
    #         for detail in [origin_detail, substitute_detail]:
    #             for product in detail:

    #                 id = product[0]
    #                 name = product[1]
    #                 brand = product[2]
    #                 qty = product[3]
    #                 store = product[4]
    #                 url = product[5]

    #                 print(message_list.pop() + "\n")
    #                 print("Nom              : {}".format(name))
    #                 print("Marque           : {}".format(brand))
    #                 print("Conditionnement  : {}".format(qty))
    #                 print("Magasins         : {}".format(store))
    #                 print("Lien OFF         : {}".format(url))
    #                 print("\n")
                    
                
    #         print("1 - Supprimer le lien")
    #         print("0 - retour")
    #         answer = input("\nVotre choix : ")
            
    #         try:
    #             answer = int(answer)
    #             if answer in range(2):
    #                 if answer:
    #                     self.db.delete_substitute(id_Substitute)
    #                 else:
    #                     self.current_screen.pop()
    #                 break
    #         except:
    #             pass

    @staticmethod
    def clear():
        """Clear console."""
        if os.uname()[0] == "Windows":
            os.system('cls')
        else:
            os.system('clear')

if __name__ == "__main__":
    gui = Gui()
    # while len(gui.current_screen):
    #     gui.screen_select()
    pass
