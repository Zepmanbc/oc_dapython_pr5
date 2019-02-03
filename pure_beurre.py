#! /usr/bin/env python3
"""Application Pure Beurre pour bien manger."""
import sys

sys.path.append('app/')
from app.gui.gui import Gui

def main():
    """Manage the screens sequences."""
    gui = Gui()
    intro = True
    while intro:
        intro = gui.screen_intro()
        if intro == 1:
            category = True
            while category:
                category = gui.screen_category()
                if category:
                    type_product = True
                    while type_product:
                        type_product = gui.screen_type_product(category)
                        if type_product:
                            product = True
                            while product:
                                product = gui.screen_product(type_product)
                                if product:
                                    while gui.screen_show_product(product):
                                        pass
        elif intro == 2:
            favorite = True
            while favorite:
                favorite = gui.screen_show_favorite()
                if favorite:
                    while gui.screen_show_product(favorite):
                        pass


if __name__ == "__main__":
    main()