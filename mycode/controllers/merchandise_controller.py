import tkinter as tk
from views.view_main import View
from models.combined_model import CombinedModel
import logging
from constants import INITIAL_DATA

logging.basicConfig(filename="debug.log",
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


class MerchandiseController:
    """
    MerchandiseController is the controller for the
    Merchandise Page. It deals with all user input from the
    Merchandise page and makes different calls for these events
    with most calls being to the MerchandiseModel.
    """
    def __init__(self, view: View, model: CombinedModel):

        """
        Constructor uses View Object to set current page
        to MerchandiseView and sets CombinedModel object to
        MerchandiseModel.

        Binds events from Merchandise Page to their handlers
        and reads in data from Merchandise table into page.

        Parameters:
            view(View) : The View object used to set current page
            model(CombinedModel) : Used to set model for merch page
        """
        self.logger = logging.getLogger(__name__)
        self.view = view
        self.current_page = self.view.pages["merchandise"]

        self.model = model.merchandise_model
        self.model.create_merchandise_table()
        self.model.insert_initial_merchandise(INITIAL_DATA)

        self._bind()
        self._read_data_into_treeview()

    def _bind(self):
        """
        Binds events from the user clicking buttons on the Merchandise
        Page to their event handlers.
        """

        self.current_page.back_button.config(
            command=self._display_home_page)

        self.current_page.select_button.config(
            command=self._display_selected_record_in_boxes)

        self.current_page.remove_button.config(
            command=self._delete_record)

        self.current_page.update_button.config(
            command=self._update_record)

        self.current_page.add_button.config(
            command=self._create_record)

        self.current_page.refresh_page_button.config(
            command=self._refresh_page)

    def _display_home_page(self):
        self.logger.info("Switching to Home Page")
        self.view.switch("home")

    # Methods to do with updating page with new data

    def _refresh_page(self):
        self._update_data_in_treeview()
        self._clear_entry_boxes()

    def _update_data_in_treeview(self):
        for child in self.current_page.my_tree.get_children():
            self.current_page.my_tree.delete(child)

        self._read_data_into_treeview()

    def _display_selected_record_in_boxes(self):
        # Clear old values in boxes before inserting new values
        self._clear_entry_boxes()

        data = self.current_page.my_tree.focus()
        data = self.current_page.my_tree.item(data)
        data = data['values']

        # Set new values for entry boxes
        self.current_page.id_entry.insert(0, data[0])
        self.current_page.product_type_entry.insert(0, data[1])
        self.current_page.description_entry.insert(0, data[2])
        self.current_page.price_entry.insert(0, data[3])
        self.current_page.quantity_entry.insert(0, data[4])

        self.current_page.id_entry.config(state="readonly")

    def _clear_entry_boxes(self):
        # Delete old values in entry boxes
        self.current_page.id_entry.config(state="normal")
        self.current_page.id_entry.delete(0, tk.END)
        self.current_page.product_type_entry.delete(0, tk.END)
        self.current_page.description_entry.delete(0, tk.END)
        self.current_page.price_entry.delete(0, tk.END)
        self.current_page.quantity_entry.delete(0, tk.END)

    # CRUD Operations
    def _create_record(self):
        """
        Creates new record in the Merchandise Table
        using Merchandise Model.
        """

        self.current_page.id_entry.config(state="normal")
        self.model.product_type = self.current_page.product_type_entry.get()
        self.model.description = self.current_page.description_entry.get()
        self.model.price = self.current_page.price_entry.get()
        self.model.quantity = self.current_page.quantity_entry.get()
        self.model.add_record()

        # Update Page
        self._clear_entry_boxes()
        self._update_data_in_treeview()

    def _read_data_into_treeview(self):
        # inserts records from DB into Treeview on UI
        data: list[tuple] = self.model.retrieve_all_records()
        for record in data:
            self.current_page.my_tree.insert(parent='',
                                             index='end',
                                             text="",
                                             values=(record[0],
                                                     record[1],
                                                     record[2],
                                                     record[3],
                                                     record[4]))

    def _update_record(self):
        """
        Updates existing record in Merchandise table using
        Merchandise Model.
        """

        self.current_page.id_entry.config(state="normal")
        self.model.id = self.current_page.id_entry.get()
        self.model.product_type = self.current_page.product_type_entry.get()
        self.model.description = self.current_page.description_entry.get()
        self.model.price = self.current_page.price_entry.get()
        self.model.quantity = self.current_page.quantity_entry.get()
        self.model.update_record()

        # Update Page
        self._clear_entry_boxes()
        self._update_data_in_treeview()

    def _delete_record(self):
        """
        Deletes record from DB with the ID retrieved from
        ID entry box on the Merchandise Page using the
        Merchandise Model.
        """

        self.current_page.id_entry.config(state="normal")
        record_id = self.current_page.id_entry.get()

        self.model.id = record_id
        self.model.delete_record()

        # Update Page
        self._clear_entry_boxes()
        self._update_data_in_treeview()
