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
            "screen_show_substitute_saved": self.screen_show_substitute_saved
        }
        self.db = Database()
        
        # if not self.db.mydb:
        try:
            self.db.cursor
        except:
            self.clear()
            print("Création de la base...")
            self.db.create_database()
            print("Récupération des données en cours...")
            self.db.fill_in_database()
        self.current_screen = [("screen_intro",)]
    
    def screen_select(self):
        """Display the last screen in current_screen.
        
        screen item is a Tuple
        ("screen_name", *args)
        """
        self.clear()
        screen = self.current_screen[-1]
        self.screen_config[screen[0]](*screen[1:])

    def screen_intro(self):
        """Print the intro screen."""
        print("""
        1 - Quel aliment souhaitez-vous remplacer ? 
        2 - Retrouver mes aliments substitués.

        0 - Quitter
        """)
        answer = input("Votre choix : ")
        try:
            answer = int(answer)
            if answer == 1:
                self.current_screen.append(("screen_select_category", ))
            elif answer == 2:
                self.current_screen.append(("screen_show_substitute_saved", 0, 0))
            elif answer == 0:
                self.current_screen.pop()
        except:
            pass

    def screen_select_category(self):
        category_list = self.db.get_category()
        self._print_list(category_list)
        print("\n0 - Retour")
        answer = input("Votre choix : ")
        try:
            answer = int(answer)
            if answer in range(len(category_list) + 1):
                if answer == 0:
                    self.current_screen.pop()
                else:
                    target_screen = "screen_select_product"
                    target_id = category_list[answer - 1][0]
                    page = 0
                    self.current_screen.append((target_screen, target_id, page))
        except:
            pass

    def _print_list(self,product_list):
        number = 0
        for product in product_list:
            number += 1
            print("{} - {}".format(number, product[1]))

    def _print_page(self, current_page, total_page):
        page_text = []
        if current_page is not 1: 
            page_text.append("[P] <-- ")
        page_text.append("page {}/{}".format(current_page, total_page))
        if current_page is not total_page: 
            page_text.append(" --> [N]")
        print(" ".join(page_text))

    def _change_page(self, max_page,  direction):
        (screen, screen_id, page) = self.current_screen[-1]
        max_page -= 1  # page is set from 0, not max_page

        if direction.upper() == "N" and page < max_page:
            self.current_screen[-1] = (screen, screen_id, page + 1)
            return True
        elif direction.upper() == "P" and page > 0:
            self.current_screen[-1] = (screen, screen_id, page - 1)
            return True
        return False

    def screen_select_product(self, category_id, page):
        if not self.db.pagination_list["product"]:
            self.db.get_product(category_id)
        max_page = len(self.db.pagination_list["product"])
        product_list = self.db.pagination_list["product"][page]
        print("Séléctionnez un produit :")
        self._print_list(product_list)
        self._print_page(page + 1, max_page)

        answer = input("\nVotre choix : ")
        if answer.upper() in "NP":
            self._change_page(max_page, answer)
        elif answer == '0':
            self.db.pagination_list["product"].clear()
            self.current_screen.pop()
        elif answer in "123456789":
            answer = int(answer)
            target_screen = "screen_select_substitute"
            target_id = product_list[answer - 1][0]
            page = 0
            self.current_screen.append((target_screen, target_id, page))
        
    def screen_select_substitute(self, origin_id, page):
        if not self.db.pagination_list["substitute"]:
            self.db.get_better_product(origin_id)
        max_page = len(self.db.pagination_list["substitute"])
        product_list = self.db.pagination_list["substitute"][page]
        print("Sélectionnez un substitut :")
        self._print_list(product_list)
        self._print_page(page + 1, max_page)

        answer = input("\nVotre choix : ")
        if answer.upper() in "NP":
            self._change_page(max_page, answer)
        elif answer == '0':
            self.db.pagination_list["substitute"].clear()
            self.current_screen.pop()
        elif answer in "123456789":
            answer = int(answer)
            target_screen = "screen_detail_substitute"
            target_id = product_list[answer - 1][0]
            self.current_screen.append((target_screen, origin_id, target_id))

    def screen_detail_substitute(self, origin_id, substitute_id):
        (origin_designation, origin_grade, substitute_designation, substitute_grade, \
            url, stores, substitute_exist) = self.db.show_product_detail(origin_id, substitute_id)[0]
        print("Produit d'origine :\n    {}".format(origin_designation))
        print("    nutrition grade : {}\n".format(origin_grade))
        print("Produit de substitution :\n    {}".format(substitute_designation))
        print("    nutrition grade : {}".format(origin_grade))
        print("    magasins : {}".format(stores))
        print("    url : {}".format(url))
        print("\nRetour : 0")
        if substitute_exist:
            print("Combinaison existante, pour la supprimer : 1")
        else:
            print("Pour enregistrer la combinaisons : 1")

        answer = input("\nVotre choix : ")
        if answer == '0':
            self.current_screen.pop()
        elif answer == '1':
            if substitute_exist:
                self.db.delete_substitute(substitute_exist)
            else:
                self.db.set_substitute(origin_id, substitute_id)
        # ajouter le switch de sauvegarde

    def screen_show_substitute_saved(self, dummy, page):
        # if not self.db.pagination_list["saved_substitute"]:
        self.db.pagination_list["saved_substitute"].clear()
        self.db.get_substitute_saved()
        max_page = len(self.db.pagination_list["saved_substitute"])
        if not max_page:
            input("Pas de substitut enregistré\nAppuyez sur [Enter]...")
            self.db.pagination_list["saved_substitute"].clear()
            self.current_screen.pop()
            return
        if page >= max_page : page = max_page - 1  # in case delete on a 1 element page
        product_list = self.db.pagination_list["saved_substitute"][page]
        print("Sélectionnez une combinaison :")
        self._print_list(product_list)
        self._print_page(page + 1, max_page)

        print("\nRetour : 0")
        answer = input("\nVotre choix : ")
        if answer.upper() in "NP":
            self._change_page(max_page, answer)
        elif answer == '0':
            self.db.pagination_list["saved_substitute"].clear()
            self.current_screen.pop()
        elif answer in "123456789":
            answer = int(answer)
            target_screen = "screen_detail_substitute"
            origin_id = product_list[answer - 1][2]
            substitute_id = product_list[answer - 1][4]
            self.current_screen.append((target_screen, origin_id, substitute_id))

    @staticmethod
    def clear():
        """Clear console."""
        if os.uname()[0] == "Windows":
            os.system('cls')
        else:
            os.system('clear')

if __name__ == "__main__":
    gui = Gui()
    # gui.current_screen.append(("screen_select_product", 1, 0))
    # gui.clear()
    # gui.screen_detail_substitute(12,34)
    # gui.current_screen.append(("screen_detail_substitute", 12 , 34))
    while len(gui.current_screen):
        gui.screen_select()
    pass
