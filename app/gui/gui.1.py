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
            "screen_show_substitute_list": self.screen_show_substitute_list
        }
        
        self.product_list = []

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
        self.clear()
        screen = self.current_screen[-1]
        print(1)
        self.screen_config[screen[0]](*screen[1:])

    def screen_intro(self):
        """Print the intro screen."""
        while True:
            # self.clear()
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
                    self.current_screen.append(("screen_show_substitute_list", 0))
                elif answer == 0:
                    self.current_screen.pop()
                break
            except:
                pass

    def screen_select_category(self):
        while True:
            category_list = self.db.get_category()
            number = 0
            print("Selectionnez une catégorie:\n")
            for category in category_list:
                number += 1
                print("{} - {}".format(number, category[1]))
            print("\n0 - Retour")
            answer = input("Votre choix : ")
            try:
                answer = int(answer)
                if answer in range(len(category_list) + 1):
                    if answer == 0:
                        self.current_screen.pop()
                    else:
                        self.current_screen.append(("screen_select_product", category_list[answer - 1][0], 0))
                break
            except:
                pass

    def _print_product_list(self,product_list):
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

    def _answer(self, product_list, current_list, name_list,  next_screen, origin_id=0):
        max_page = len(current_list)
        print("\n0 - Retour")
        answer = input("Votre choix : ")
        try:
            answer = int(answer)
            if answer in range(len(product_list) + 1):
                if answer == 0:
                    self.current_screen.pop()
                    if name_list == "get_substitute_saved": self.db.get_substitute_saved = []
                    elif name_list == "random_result": self.db.random_result = []
                    elif  name_list == "substitute_proposition": self.db.substitute_proposition = []
                else:
                    if next_screen == "screen_detail_substitute":
                        self.current_screen.append((next_screen, product_list[answer - 1][0], origin_id))
                    else:
                        self.current_screen.append((next_screen, product_list[answer - 1][0], 0))
            return True
        except:
            self._change_page(max_page, answer)
            return True
        return False

    def screen_select_product(self, category_id, page):
        if not self.db.random_result:
            self.db.get_product(category_id)
        max_page = len(self.db.random_result)
        product_list = self.db.random_result[page]
        print("Séléctionnez un produit :")
        self._print_product_list(product_list)
        self._print_page(page + 1, max_page)
        self._answer(product_list, self.db.random_result, "random_result", "screen_select_substitute")
    
    def screen_select_substitute(self, product_id, page):
        if not self.db.substitute_proposition:
            self.db.get_better_product(product_id)
        max_page = len(self.db.substitute_proposition)
        product_list = self.db.substitute_proposition[page]
        print("Sélectionnez un substitut :")
        self._print_product_list(product_list)
        self._print_page(page + 1, len(self.db.substitute_proposition))
        self._answer(product_list, self.db.substitute_proposition, "substitute_proposition",\
            "screen_detail_substitute", product_id)

    def screen_detail_substitute(self, origin_id, subtitute_id):
        print("screen_detail_substitute")
        # detail = self.db.show_product_detail(origin_id, subtitute_id)
        (origin_designation, origin_grade, substitute_designation, substitute_grade, \
            url, stores) = self.db.show_product_detail(origin_id, subtitute_id)[0]
        print("Produit d'origine :\n    {}".format(origin_designation))
        print("    nutrition grade : {}\n".format(origin_grade))
        print("Produit de substitution :\n    {}".format(substitute_designation))
        print("    nutrition grade : {}".format(origin_grade))
        print("    magasins : {}".format(stores))
        print("    url : {}".format(url))

        # ajouter le switch de sauvegarde

    def screen_show_substitute_list(self, page):
        if not self.db.substitute_saved:
            self.db.get_substitute_saved()
        max_page = len(self.db.substitute_saved)
        if max_page:
            product_list = self.db.substitute_saved[page]
            print("Séléctionnez une combinaison :")
            self._print_product_list(product_list)
            self._print_page(page + 1, max_page)
            # self._answer(product_list, self.db.substitute_saved, "get_substitute_saved",\
            #     "screen_detail_substitute", )

            print("\n0 - Retour")
            answer = input("Votre choix : ")
            try:
                answer = int(answer)
                if answer in range(len(product_list) + 1):
                    if answer == 0:
                        self.current_screen.pop()
                        self.db.get_substitute_saved = []
                    else:
                        self.current_screen.append(("screen_detail_substitute", product_list[answer - 1][2], product_list[answer - 1][4]))
            except:
                self._change_page(max_page, answer)
        else:
            self.current_screen.pop()
            input("Il n'y a pas de produit de substitution sauvegardé\nAppuyez sur [Enter]...")

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
