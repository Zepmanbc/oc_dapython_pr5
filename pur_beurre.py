#! /usr/bin/env python3
"""Application Pur Beurre pour bien manger."""
import sys

sys.path.append('app/')
from app.gui.gui import Gui
import config

def main():
    """Run the software."""
    gui = Gui(config.dbconnect)
    if hasattr(gui, "current_screen") and gui.db.mydb:
        while len(gui.current_screen):
            gui.screen_select()   

if __name__ == "__main__":
    main()