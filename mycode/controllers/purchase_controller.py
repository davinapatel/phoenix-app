import tkinter as tk
import logging
from views.view_main import View
from models.combined_model import CombinedModel

logging.basicConfig(filename="debug.log",
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


class PurchaseController:
    """
    The PurchaseController is the controller for the Purchase Page.
    It receives input from the Purchase Page and makes calls based
    on the input, usually makes calls to PurchaseModel
    """
    def __init__(self, view: View, model: CombinedModel):
        """
        Constructor uses View Object to set current page
        to PurchaseView and sets CombinedModel object to
        PurchaseModel.

        Binds events from Purchase Page to their handlers
        and reads in data from Purchase table into page.

        Parameters:
            view (View) : The View object used to set current page
            model (CombinedModel) : Used to set model for purchase page
        """
        self.logger = logging.getLogger(__name__)
        self.view = view

        self.merchandise_model = model.merchandise_model
        self.purchase_model = model.purchase_model
        self.purchase_model.create_purchase_table()

        self.current_page = self.view.pages["purchase"]
        self._bind()
        self._update_page()

    def _bind(self):
        """
        Binds events from users clicking buttons on the Purchase
        Page to their event handlers.
        """

        self.current_page.back_button.config(
            command=self._display_home_page)

        self.current_page.create_purchase_button.config(
            command=self._create_purchase)

        self.current_page.product_type_button.bind(
            "<<ComboboxSelected>>",
            lambda x: self._insert_quantities())

        self.current_page.quantity_button.bind(
            "<<ComboboxSelected>>",
            lambda x: self._insert_cost_and_date())

        self.current_page.cancel_purchase_button.config(
            command=self._cancel_purchase)

        self.current_page.refresh_button.config(
            command=self._update_page)

    def _display_home_page(self):
        self.logger.info("Switching to Home Page")
        self.view.switch("home")

    def _create_purchase(self):
        """
        Takes input from the Purchase Page and uses
        the Purchase model to create an entry in the Purchase
        table.
        """
        # Gets values from the entry boxes on the page
        product_type = self.current_page.product_type_button.get()
        quantity = self.current_page.quantity_button.get()
        total_cost = self.current_page.total_cost_button.get()
        date = self.current_page.date_button.get()
        merch_id = self.merchandise_model.retrieve_id(product_type)

        self.purchase_model.product_type = product_type
        self.purchase_model.quantity = quantity
        self.purchase_model.total_cost = total_cost
        self.purchase_model.date = date
        self.purchase_model.merchandise_id = merch_id

        # old_quantity: int = self.merchandise_model.retrieve_quantity(
        #     product_type)
        # new_quantity: int = self.purchase_model.calculate_new_quantity(
        #     old_quantity)
        # self.merchandise_model.update_quantity(product_type, new_quantity)

        self._calculate_new_quantity(product_type)

        self.purchase_model.create_record()

        # Update page by removing old values and reinserting
        self.current_page.date_button.delete(0, tk.END)
        self.current_page.total_cost_button.delete(0, tk.END)

        self._insert_quantities()
        self._insert_order_ids_into_button()
        self._update_data_in_treeview()
        self._clear_buttons()

    def _calculate_new_quantity(self, product_type):
        """
        Calculates the new quantity for the product
        after a purchase has been made to update the quantity
        for it in the merchandise table.
        """
        old_quantity: int = self.merchandise_model.retrieve_quantity(
            product_type)
        new_quantity: int = self.purchase_model.calculate_new_quantity(
            old_quantity)
        self.merchandise_model.update_quantity(product_type, new_quantity)

    def _clear_buttons(self):
        self.current_page.purchase_id_button.set("")
        self.current_page.product_type_button.set("")
        self.current_page.quantity_button.set("")

    def read_product_types(self):
        """
        Reads in the Product Types from the Merchandise table
        into the buttons in the PurchaseView
        """
        product_types = self.merchandise_model.retrieve_all_product_types()
        cleaned_data = []
        for record in product_types:
            # cleaned_data.append(record[0])
            product_type = record[0]
            quantity = self.merchandise_model.retrieve_quantity(product_type)
            if quantity != 0:
                cleaned_data.append(product_type)

        self.current_page.product_type_button['values'] = tuple(cleaned_data)

    def _insert_quantities(self):
        """
        Reads in the quantity of the selected Product Type
        from the Merchandise table and inserts into
        Purchase Page.
        """
        product_type = self.current_page.product_type_button.get()
        count = self.merchandise_model.retrieve_count(product_type)
        quantities = []
        for x in range(1, count + 1):
            quantities.append(x)
        quantities = tuple(quantities)
        self.current_page.quantity_button['values'] = quantities
        self.read_product_types()

    def _insert_cost_and_date(self):
        """
        Inserts the total cost for Purchase and today's
        date into entry boxes in PurchaseView.
        """
        product_type = self.current_page.product_type_button.get()
        self.purchase_model.quantity = self.current_page.quantity_button.get()

        price_of_product = float(self.merchandise_model.retrieve_price(
            product_type))

        total_cost, today_date = self.purchase_model.calculate_cost_and_date(
            price_of_product)

        self.current_page.total_cost_button.insert(0, total_cost)
        self.current_page.date_button.insert(0, today_date)

    def _update_data_in_treeview(self):
        for child in self.current_page.my_tree.get_children():
            self.current_page.my_tree.delete(child)

        self._insert_data_into_table()

    def _insert_data_into_table(self):
        """
        Inserts data read in from the Purchase and Merchandise
        table to show all relevant data for Purchases made onto
        Purchase Page.
        """
        data: list[tuple] = self.purchase_model.retrieve_all_records()
        for record in data:
            merch_id = record[1]
            product_type = self.merchandise_model.retrieve_product_type(
                merch_id)
            description = self.merchandise_model.retrieve_description(merch_id)
            price = float(self.merchandise_model.retrieve_price(
                product_type))
            self.current_page.my_tree.insert(parent='',
                                             index='end',
                                             text="",
                                             values=(record[0],
                                                     product_type,
                                                     description,
                                                     price,
                                                     record[2],
                                                     record[3],
                                                     record[4]))

    def _insert_order_ids_into_button(self):
        """
        Inserts the Purchase Order IDs into Purchase View
        so they can be selected to cancel a Purchase
        """
        purchase_ids = self.purchase_model.retrieve_all_ids()
        cleaned_data = []
        for record in purchase_ids:
            cleaned_data.append(record[0])

        self.current_page.purchase_id_button['values'] = tuple(cleaned_data)

    def _update_page(self):
        self._update_data_in_treeview()
        self._insert_order_ids_into_button()
        self.read_product_types()

    def _cancel_purchase(self):
        """
        Cancels Purchase that user has selected from Purchase Page
        and makes calls to Purchase Model to remove entry from
        Purchase Table.
        """
        self.purchase_model.id = self.current_page.purchase_id_button.get()

        # update stock
        merch_id = self.purchase_model.retrieve_merch_id()
        quantity_to_add = self.purchase_model.retrieve_quantity()
        self.merchandise_model.increase_merch_quantity(merch_id,
                                                       quantity_to_add)
        self.purchase_model.delete_record()

        self.current_page.purchase_id_button.set("")
        self._update_page()
