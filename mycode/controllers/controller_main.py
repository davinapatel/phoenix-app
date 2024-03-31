from views.view_main import View
from .home_controller import HomeController
from .merchandise_controller import MerchandiseController
from .purchase_controller import PurchaseController
from .sales_breakdown_controller import SalesController
from models.combined_model import CombinedModel
import logging
import sqlite3

logging.basicConfig(filename="debug.log",
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


class Controller:
    """
    The Controller class acts a base class for the other controllers
    which are specific to each page.
    This class stores all the controller objects.
    """

    def __init__(self, db_name: str):
        """
        Constructor connects to sqlite DB,
        instantiates the CombinedModel and
        instantiates all controller objects specific to each
        page.

        Parameter:
            db_name(str) : Name of DB file to connect to

        """
        self.view = View()
        self.logger = logging.getLogger(__name__)
        self.connection = self.connect_to_db(db_name)
        self.combined_model = CombinedModel(self.connection)
        self.home_controller = HomeController(self.view)
        self.merchandise_controller = MerchandiseController(
                                                    self.view,
                                                    self.combined_model)
        self.purchase_controller = PurchaseController(self.view,
                                                      self.combined_model)
        self.sales_controller = SalesController(self.view,
                                                self.combined_model)

    def start(self):
        """
        Displays Home Page as first page when application starts
        and starts main loop.
        """

        self.logger.info("Switching to home page")
        self.view.switch("home")
        self.view.start_main_loop()

    def connect_to_db(self, filename: str) -> sqlite3.Connection:
        """
        Connects to Phoenix Database and enables foreign keys

        Parameter:
            filename(str) : Name of file to connect to
        Returns:
            Sqlite3 Connection Object : connection """

        connection = sqlite3.connect(filename)
        connection.execute("PRAGMA foreign_keys = 1")
        self.logger.info("Successfully connected to Phoenix DB")
        return connection
