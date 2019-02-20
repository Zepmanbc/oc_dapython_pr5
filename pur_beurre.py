#! /usr/bin/env python3
"""Application Pur Beurre pour bien manger."""
import sys

import config
# sys.path.append('app/')
from app.gui.gui import Gui

def main():
    """Run the software."""
    gui = Gui(config.DBCONNECT)
    if hasattr(gui, "current_screen") and gui.db.mydb:
        while gui.current_screen:
            gui.screen_select()

if __name__ == "__main__":
    main()
