from tkinter import Button, Entry, Frame, Label, ttk, Scrollbar, LabelFrame
import tkinter


class PurchaseView(Frame):
    """
    The PurchaseView class creates the Purchase Page.
    It inherits from Tkinter Frame.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header = ttk.Label(self, text="Purchases")
        self.header.config(font=("Arial", 20))
        self.header.pack()

        self.subheader = ttk.Label(self, text="List of Purchases Made")
        self.subheader.config(font=("Arial", 12))
        self.subheader.pack(pady=15)

        self.tree_frame = Frame(self)
        self.tree_frame.pack(pady=20)
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
                                   "QUANTITY",
                                   "TOTAL_COST",
                                   "DATE")
        self.my_tree.column("#0", width=0, stretch=False)
        self.my_tree.column("ID", anchor='w', width=110)
        self.my_tree.column("PRODUCT_TYPE", anchor='w', width=110)
        self.my_tree.column("DESCRIPTION", anchor='w', width=110)
        self.my_tree.column("PRICE", anchor='w', width=110)
        self.my_tree.column("QUANTITY", anchor='w', width=110)
        self.my_tree.column("TOTAL_COST", anchor='w', width=110)
        self.my_tree.column("DATE", anchor='w', width=110)

        self.my_tree.heading("#0", text="", anchor='center')
        self.my_tree.heading("ID", text="ID", anchor='center')
        self.my_tree.heading("PRODUCT_TYPE",
                             text="Product Type",
                             anchor='center')
        self.my_tree.heading("DESCRIPTION",
                             text="Description",
                             anchor='center')
        self.my_tree.heading("PRICE", text="Price(£)", anchor='center')
        self.my_tree.heading("QUANTITY", text="Quantity", anchor='center')
        self.my_tree.heading("TOTAL_COST",
                             text="Total Cost(£)",
                             anchor='center')
        self.my_tree.heading("DATE", text="Date", anchor='center')

        self.cancel_purchase_frame = LabelFrame(self, text="Cancel Purchase")
        self.cancel_purchase_frame.pack(fill="x", expand="yes", padx=20)

        self.purchase_id_label = Label(self.cancel_purchase_frame,
                                       text="Purchase ID")
        self.purchase_id_label.grid(row=0, column=2, padx=10, pady=10)

        purchase_id = tkinter.StringVar()
        self.purchase_id_button = ttk.Combobox(self.cancel_purchase_frame,
                                               width=20,
                                               textvariable=purchase_id)
        self.purchase_id_button.grid(row=0, column=3, padx=10, pady=10)

        self.cancel_purchase_button = Button(self.cancel_purchase_frame,
                                             text="Cancel Purchase")
        self.cancel_purchase_button.grid(row=0, column=10, padx=10, pady=10)

        self.create_purchase_frame = LabelFrame(self, text="Create Purchase")
        self.create_purchase_frame.pack(fill="x", expand="yes", padx=20)

        self.product_type_label = Label(self.create_purchase_frame,
                                        text="Product Type")
        self.product_type_label.grid(row=0, column=2, padx=10, pady=10)

        product_type = tkinter.StringVar()
        self.product_type_button = ttk.Combobox(self.create_purchase_frame,
                                                width=20,
                                                textvariable=product_type)

        self.product_type_button.grid(row=0, column=3, padx=10, pady=10)
        self.product_type_button.current()

        self.quantity_label = Label(self.create_purchase_frame,
                                    text="Quantity")
        self.quantity_label.grid(row=0, column=4, padx=10, pady=10)

        quantity = tkinter.StringVar()
        self.quantity_button = ttk.Combobox(self.create_purchase_frame,
                                            width=20,
                                            textvariable=quantity)

        self.quantity_button.grid(row=0, column=5, padx=10, pady=10)
        self.quantity_button.current()

        self.total_cost_label = Label(self.create_purchase_frame,
                                      text="Total Cost(£)")
        self.total_cost_label.grid(row=0, column=6, padx=10, pady=10)

        total_cost = tkinter.StringVar()
        self.total_cost_button = Entry(self.create_purchase_frame,
                                       textvariable=total_cost)
        self.total_cost_button.grid(row=0, column=7, padx=10, pady=10)

        self.date_label = Label(self.create_purchase_frame, text="Date")
        self.date_label.grid(row=1, column=2, padx=10, pady=10)

        date = tkinter.StringVar()
        self.date_button = Entry(self.create_purchase_frame,
                                 textvariable=date)
        self.date_button.grid(row=1, column=3, padx=10, pady=10)

        self.create_purchase_button = Button(self.create_purchase_frame,
                                             text="Create Purchase")
        self.create_purchase_button.grid(row=1, column=10, padx=10, pady=10)

        self.refresh_button = Button(self, text="Refresh Page")
        self.refresh_button.pack()

        self.back_button = Button(self, text="Back to Home Page")
        self.back_button.pack()
