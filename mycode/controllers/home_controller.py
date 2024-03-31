from views.view_main import View
import logging

logging.basicConfig(filename="debug.log",
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


class HomeController:
    """
    HomeController class is the controller for the Home Page.
    It deals with all user input from the Home Page and makes different
    calls for these events.
    """
    def __init__(self, view: View):

        """
        Constructor sets the current page to be the HomeView
        and binds the events that can be triggered from the Home
        Page to their event handlers.

        Parameter:
            view(View) : View object used to set the current page
        """
        self.logger = logging.getLogger(__name__)
        self.view = view
        self.current_page = self.view.pages["home"]
        self._bind()

    def _bind(self):
        """
        Binds events from users clicking buttons
        on the Home Page to their event handler.
        """

        self.current_page.merchandise_button.config(
            command=self.display_merchandise_page)

        self.current_page.purchase_button.config(
            command=self.display_purchase_page)

        self.current_page.sales_breakdown_button.config(
            command=self._display_sales_breakdown_page)

    def display_merchandise_page(self):
        """
        Calls the switch method from the View class to display
        the Merchandise page.
        """
        self.logger.info("Switching to Merchandise Page")
        self.view.switch("merchandise")

    def display_purchase_page(self):
        """
        Calls the switch method from the View class to
        display the Purchase Page.
        """
        self.logger.info("Switching to Purchase Page")
        self.view.switch("purchase")

    def _display_sales_breakdown_page(self):
        """
        Calls the switch method from the View class to
        display the Sales Breakdown Page.
        """
        self.logger.info("Switching to Sales Breakdown Page")
        self.view.switch("sales_breakdown")
