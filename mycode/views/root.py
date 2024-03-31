from tkinter import Tk
from constants import WINDOW_TITLE, WINDOW_HEIGHT, WINDOW_WIDTH


class Root(Tk):

    """ Creates the Tkinter root window for application. """

    def __init__(self):

        """ Constructor sets the geometry and title for root window. """
        super().__init__()
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.title(WINDOW_TITLE)
        self.resizable(False, False)
