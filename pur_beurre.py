#! /usr/bin/env python3
"""Application Pur Beurre pour bien manger."""
import sys

sys.path.append('app/')
from app.gui.gui import Gui

def main():
    """Manage the screens sequences."""
    gui = Gui()
    loop = True
    while len(gui.current_screen):
        gui.screen_select()

if __name__ == "__main__":
    main()