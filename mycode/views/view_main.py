from .root import Root
from .home_view import HomeView
from .merchandise_view import MerchandiseView
from .purchase_view import PurchaseView
from .sales_breakdown_view import SalesBreakdownView
from tkinter import Frame


class View():

    """
    The View class acts as a container class for all views.
    Pages are created and stored in this class. This class will raise
    a specific page(frame) to the front of the tkinter window to display it
    """
    def __init__(self):
        """ Creates root window and stores separate pages for application. """
        self.root = Root()
        self.pages = {}

        self._add_page(HomeView, "home")
        self._add_page(MerchandiseView, "merchandise")
        self._add_page(PurchaseView, "purchase")
        self._add_page(SalesBreakdownView, "sales_breakdown")

    def _add_page(self, frame: Frame, name: str):
        """
        Stores the separate pages in the pages attribute

            Parameters:
                frame (object) : Tkinter frame for a specific page
                name (str) : Name of the page

        """
        self.pages[name] = frame(self.root)
        self.pages[name].grid(row=0, column=0, sticky="nsew")

    def switch(self, name: str):
        """ Method used to switch the page displayed on application window.

            Parameters:
                name (str) : Name of the page to display"""
        page = self.pages[name]
        page.tkraise()

    def start_main_loop(self):
        """ Method used to start the Tkinter event loop. """
        self.root.mainloop()
