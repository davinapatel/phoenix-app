import tkinter as tk
import logging
from views.view_main import View
from models.combined_model import CombinedModel

logging.basicConfig(filename="debug.log",
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


class SalesController:
    """
    The SalesController class acts as a controller for the Sales Page.
    It receives input from the SalesBreakdown View and then calls
    the corresponding event handlers.
    """

    def __init__(self, view: View, model: CombinedModel):
        """
        Constructor uses View Object to set current page
        to SalesBreakdownView and sets CombinedModel object to
        PurchaseModel and MerchandiseModel as needs to access
        both.

        Binds events from Sales Page to their handlers.

        Parameters:
            view(View) : The View object used to set current page
            model(CombinedMode) : Used to set models
        """
        self.logger = logging.getLogger(__name__)
        self.view = view
        self.purchase_model = model.purchase_model
        self.merchandise_model = model.merchandise_model
        self.current_page = self.view.pages["sales_breakdown"]
        self._bind()

    def _bind(self):
        """
        Binds events to their event handlers which will be called
        when the user triggers an event from clicking a button
        on the Sales Breakdown Page
        """

        self.current_page.back_button.config(
            command=self._display_home_page)

        self.current_page.refresh_button.config(
            command=self._refresh_page)

        self.current_page.clear_db_button.config(
            command=self._clear_db)

    def _display_home_page(self):
        self.logger.info("Switching to Home Page")
        self.view.switch("home")

    def _refresh_page(self):

        for child in self.current_page.my_tree.get_children():
            self.current_page.my_tree.delete(child)

        self.current_page.cost_to_band_button.delete(0, tk.END)

        self._insert_data_into_page()

    def _insert_data_into_page(self):

        # Inserts data into the treeview
        records, total_for_band = self.purchase_model.calculate_sales()
        if records != []:
            for record in records:
                merch_id = record[0]
                product_type = self.merchandise_model.retrieve_product_type(
                    merch_id)
                self.current_page.my_tree.insert(parent='',
                                                 index='end',
                                                 values=(
                                                    product_type,
                                                    record[1],
                                                    record[2],
                                                    record[3],
                                                    record[4]
                                                 ))

        # Inserts data into the total cost to pay band button
        self.current_page.cost_to_band_button.insert(0, total_for_band)

    def _clear_db(self):
        """
        Method called to clear database and close application.
        """
        self.purchase_model.delete_purchase_table()
        self.merchandise_model.delete_merchandise_table()
        self.view.root.destroy()
