from tkinter import Frame, Scrollbar, ttk, Button, Label, LabelFrame, Entry


class MerchandiseView(Frame):

    """
    The MerchandiseView Class creates the Merchandise Page
    It inherits from Tkinter Frame.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor creates the Tkinter frontend for the Merchandise
        Page.

        Parameters:
        *args
        **kwargs
        """
        super().__init__(*args, **kwargs)

        self.header = ttk.Label(self, text="Merchandise")
        self.header.config(font=("Arial", 20))
        self.header.pack()

        self.tree_frame = Frame(self)
        self.tree_frame.pack(pady=100)
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side='right', fill='y')
        self.my_tree = ttk.Treeview(self.tree_frame,
                                    yscrollcommand=self.tree_scroll.set,
                                    selectmode="extended")
        self.my_tree.pack()

        self.tree_scroll.config(command=self.my_tree.yview)

        self.my_tree['columns'] = ("ID",
                                   "PRODUCT_TYPE",
                                   "DESCRIPTION",
                                   "PRICE",
                                   "QUANTITY")
        self.my_tree.column("#0", width=0, stretch=False)
        self.my_tree.column("ID", anchor='w', width=140)
        self.my_tree.column("PRODUCT_TYPE", anchor='w', width=140)
        self.my_tree.column("DESCRIPTION", anchor='w', width=140)
        self.my_tree.column("PRICE", anchor='w', width=140)
        self.my_tree.column("QUANTITY", anchor='w', width=140)

        self.my_tree.heading("#0", text="", anchor='center')
        self.my_tree.heading("ID", text="ID", anchor='center')
        self.my_tree.heading("PRODUCT_TYPE",
                             text="Product Type",
                             anchor='center')
        self.my_tree.heading("DESCRIPTION",
                             text="Description",
                             anchor='center')
        self.my_tree.heading("PRICE", text="Price", anchor='center')
        self.my_tree.heading("QUANTITY", text="Quantity", anchor='center')

        self.data_frame = LabelFrame(self, text="Record")
        self.data_frame.pack(fill="x", expand="yes", padx=20)

        self.id_label = Label(self.data_frame, text="ID")
        self.id_label.grid(row=1, column=0, padx=10, pady=10)
        self.id_entry = Entry(self.data_frame)
        self.id_entry.grid(row=1, column=1, padx=10, pady=10)

        self.product_type_label = Label(self.data_frame, text="Product Type")
        self.product_type_label.grid(row=0, column=2, padx=10, pady=10)
        self.product_type_entry = Entry(self.data_frame)
        self.product_type_entry.grid(row=0, column=3, padx=10, pady=10)

        self.description_label = Label(self.data_frame, text="Description")
        self.description_label.grid(row=0, column=6, padx=10, pady=10)
        self.description_entry = Entry(self.data_frame)
        self.description_entry.grid(row=0, column=7, padx=10, pady=10)

        self.price_label = Label(self.data_frame, text="Price(£)")
        self.price_label.grid(row=0, column=0, padx=10, pady=10)
        self.price_entry = Entry(self.data_frame)
        self.price_entry.grid(row=0, column=1, padx=10, pady=10)

        self.quantity_label = Label(self.data_frame, text="Quantity")
        self.quantity_label.grid(row=0, column=8, padx=10, pady=10)
        self.quantity_entry = Entry(self.data_frame)
        self.quantity_entry.grid(row=0, column=9, padx=10, pady=10)

        self.button_frame = LabelFrame(self, text="Commands")
        self.button_frame.pack(fill="x", expand="yes", padx=20)

        self.update_button = Button(self.button_frame, text="Update Record")
        self.update_button.grid(row=0, column=0, padx=10, pady=10)

        self.add_button = Button(self.button_frame, text="Add Record")
        self.add_button.grid(row=0, column=1, padx=10, pady=10)

        self.remove_button = Button(self.button_frame, text="Remove Record")
        self.remove_button.grid(row=0, column=2, padx=10, pady=10)

        self.select_button = Button(self.button_frame, text="Select Record")
        self.select_button.grid(row=0, column=3, padx=10, pady=10)

        self.refresh_page_button = Button(self.button_frame,
                                          text="Refresh Page")
        self.refresh_page_button.grid(row=0, column=4, padx=10, pady=10)

        self.back_button = Button(self, text="Back to Home Page")
        self.back_button.pack()
