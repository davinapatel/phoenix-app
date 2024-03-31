import tkinter as tk
from tkinter import Frame
from tkinter import ttk


class HomeView(Frame):

    """ The HomeView Class creates the Home Page.
    It inherits from Tkinter Frame. """

    def __init__(self, *args, **kwargs):
        """
        Constructor creates the Tkinter frontend for the Home Page.

        Parameters:
        *args
        **kwargs
        """
        super().__init__(*args, **kwargs)

        self.header_frame = tk.Frame(self)
        self.header_frame.pack()

        self.header = tk.Label(self.header_frame,
                               text="Phoenix Merchandise Application")
        self.header.config(font=("Arial", 20))
        self.header.pack(anchor="center")

        self.button_frame = tk.Frame(self)
        self.button_frame.pack()

        self.merchandise_button = ttk.Button(self.button_frame,
                                             text="Merchandise")
        self.merchandise_button.pack(ipadx=90,
                                     ipady=40,
                                     anchor="center")

        self.purchase_button = ttk.Button(self.button_frame,
                                          text="Purchase")

        self.purchase_button.pack(ipadx=90,
                                  ipady=40,
                                  anchor="center")

        self.sales_breakdown_button = ttk.Button(self.button_frame,
                                                 text="Sales Breakdown")

        self.sales_breakdown_button.pack(ipadx=90,
                                         ipady=40,
                                         anchor="center")
