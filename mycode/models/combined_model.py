from .purchase_model import PurchaseModel
from .merchandise_model import MerchandiseModel
import sqlite3


class CombinedModel:
    """
        The CombinedModel Class acts as a container class for all the models.
        It instantiates the models specific to the Purchase
        and Merchandise Page.
    """

    def __init__(self, connection: sqlite3.Connection):
        """
        Constructor instantiates and stores the PurchaseModel
        and MerchandiseModel passing each the sqlite connection
        object

            Parameters:
                connection (object) : Sqlite Connection Object
        """
        self.purchase_model = PurchaseModel(connection)
        self.merchandise_model = MerchandiseModel(connection)
