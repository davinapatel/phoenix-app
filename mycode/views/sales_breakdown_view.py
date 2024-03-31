from tkinter import Entry, Frame, Label, LabelFrame, ttk, Button, Scrollbar
import tkinter


class SalesBreakdownView(Frame):
    """
    The SalesBreakdownView creates the Sales Breakdown Page.
    It inherits from Tkinter Frame.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header = ttk.Label(self, text="Sales Breakdown")
        self.header.config(font=("Arial", 20))
        self.header.pack()

        self.tree_frame = Frame(self)
        self.tree_frame.pack(pady=10)
        self.tree_scroll = Scrollbar(self.tree_frame)

        self.my_tree = ttk.Treeview(self.tree_frame,
                                    yscrollcommand=self.tree_scroll.set,
                                    selectmode="extended")
        self.my_tree.pack()

        self.tree_scroll.config(command=self.my_tree.yview)

        self.my_tree['columns'] = ("PRODUCT TYPE",
                                   "TOTAL_SOLD",
                                   "TOTAL_COST",
                                   "TOTAL_PHOENIX",
                                   "TOTAL_BAND")
        self.my_tree.column("#0", width=0, stretch=False)
        self.my_tree.column("PRODUCT TYPE", anchor='w', width=110)
        self.my_tree.column("TOTAL_SOLD", anchor='w', width=110)
        self.my_tree.column("TOTAL_COST", anchor='w', width=110)
        self.my_tree.column("TOTAL_PHOENIX", anchor='w', width=110)
        self.my_tree.column("TOTAL_BAND", anchor='w', width=110)

        self.my_tree.heading("#0", text="", anchor='center')
        self.my_tree.heading("PRODUCT TYPE", text="Product Type",
                             anchor='center')
        self.my_tree.heading("TOTAL_SOLD", text="Total Sold", anchor='center')
        self.my_tree.heading("TOTAL_COST",
                             text="Total Cost(£)",
                             anchor='center')
        self.my_tree.heading("TOTAL_PHOENIX",
                             text="Total to pay Phoenix(£)",
                             anchor='center')
        self.my_tree.heading("TOTAL_BAND",
                             text="Total to pay Band(£)",
                             anchor='center')

        self.cost_frame = LabelFrame(self, text="Cost")
        self.cost_frame.pack(fill="x", expand="yes", padx=20)

        self.cost_to_band_label = Label(self.cost_frame,
                                        text="Total to pay Band(£)")
        self.cost_to_band_label.grid(row=0, column=2, padx=10, pady=10)

        cost = tkinter.StringVar()
        self.cost_to_band_button = Entry(self.cost_frame,
                                         textvariable=cost)
        self.cost_to_band_button.grid(row=0, column=3, padx=10, pady=10)

        self.refresh_button = Button(self, text="Refresh Page")
        self.refresh_button.pack()

        self.clear_db_button = Button(self,
                                      text="Clear DB and Close Application")
        self.clear_db_button.pack()

        self.back_button = Button(self, text="Back to Home Page")
        self.back_button.pack()
