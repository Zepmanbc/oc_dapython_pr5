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
            "screen_category": self.screen_category,
            "screen_type_product": self.screen_type_product,
            "screen_product": self.screen_product,
            "screen_show_product": self.screen_show_product,
            "screen_show_favorite": self.screen_show_favorite
        }

        self.db = Database()
        if self.db.mydb:
            self.current_screen = [("screen_intro",)]
            try:
                self.db.cursor
            except:
                self.clear()
                print("Création de la base...")
                self.db.create_database()
                print("Récupération des données en cours...")
                self.db.fill_in_database()
        else:
            self.db = False
    
    def screen_select(self):
        """Display the last screen in current_screen."""
        screen = self.current_screen[-1]
        if len(screen) == 1:
            self.screen_config[screen[0]]()
        elif len(screen) == 2:
            self.screen_config[screen[0]](screen[1])

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
                    self.current_screen.append(("screen_category",))
                elif answer == 2:
                    self.current_screen.append(("screen_show_favorite",))
                elif answer == 0:
                    self.current_screen.pop()
                break
            except:
                pass

    def screen_category(self):
        """Print category list.

        From Category TABLE.

        """
        list_category = self.db.get_category()
        while True:
            self.clear()
            for category in list_category:
                print("{} - {}".format(category[0],category[1]))
            print("\n0 - retour")
            answer = input("\nVotre choix : ")

            try:
                answer = int(answer)
                if answer in range(len(list_category) + 1):
                    if answer == 0:
                        self.current_screen.pop()
                    else:
                        self.current_screen.append(("screen_type_product", answer))
                    break
            except:
                pass

    def screen_type_product(self, category_id):
        """Print list of product type for a category.

        Args:
            category_id (int): if from Category TABLE.
        """
        list_type_product = self.db.get_type_product(category_id)
        while True:
            self.clear()
            number = 0
            for type_product in list_type_product:
                number += 1
                print("{} - {}".format(number, type_product[1]))
            print("\n0 - retour")
            answer = input("\nVotre choix : ")
            
            try:
                answer = int(answer)
                if answer in range(len(list_type_product) + 1):
                    if answer == 0:
                        self.current_screen.pop()
                    else:
                        self.current_screen.append(("screen_product", list_type_product[answer - 1][0]))
                    break
            except:
                pass

    def screen_product(self, product_id):
        """Print list of 9 products.

        Args:
            product_id (int): id of a product type from Product TABLE.

        """
        list_product = self.db.get_product(product_id)
        while True:
            self.clear()
            number = 0
            for product in list_product:
                number += 1
                # id = product[0]
                name = product[1]
                brand = product[2]
                qty = product[3]
                print("{} - {} - {} - {}".format(number, name, brand, qty))
            print("\n0 - retour")
            answer = input("\nVotre choix : ")
            
            try:
                answer = int(answer)
                if answer in range(len(list_product) + 1):
                    if answer == 0:
                        self.current_screen.pop()
                    else:
                        self.current_screen.append(("screen_show_product", list_product[answer - 1][0]))
                    break
            except:
                pass

    def screen_show_product(self, id_off):
        """Print detail of a product.

        Args:
            id_off (int): id of a product from offData TABLE.

        """
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
                    else:
                        self.current_screen.pop()
                    break
            except:
                pass

    def screen_show_favorite(self):
        """Print favorites."""
        list_product = self.db.get_favorites()
        if list_product:
            while True:
                self.clear()
                number = 0
                for product in list_product:
                    number += 1
                    id = product[0]
                    category_name = "{} - ".format(product[1])
                    product_type = "{} - ".format(product[2])
                    product_name = "{} - {} - {}".format(product[3], product[4], product[5])
                    row = category_name + product_type + product_name
                    print("{} - {}".format(number, row))
                
                print("\n0 - retour")
                answer = input("\nVotre choix : ")
                
                try:
                    answer = int(answer)
                    if answer in range(len(list_product) + 1):
                        if answer == 0:
                            self.current_screen.pop()
                        else:
                            self.current_screen.append(("screen_show_product", list_product[answer - 1][0]))
                        break
                except:
                    pass
        else:
            self.clear()
            print("*** PAS DE FAVORIS ***")
            input("appuyez sur une touche...")
    
    @staticmethod
    def clear():
        """Clear console."""
        if os.uname()[0] == "Windows":
            os.system('cls')
        else:
            os.system('clear')

if __name__ == "__main__":
    gui = Gui()
    # if not gui.current_screen in locals():
    #     gui.current_screen.append(("screen_show_favorite",))
    #     gui.screen_select()

    if not hasattr(gui, "current_screen"):
        print("C'est mort")
    # try:
    #     hasattr(gui, current_screen)
    #     gui.current_screen.append(("screen_show_favorite",))
    #     gui.screen_select()
    # except NameError:
    #     pass
    pass
