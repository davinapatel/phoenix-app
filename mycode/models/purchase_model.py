from datetime import date
import sqlite3
import logging


logging.basicConfig(filename="debug.log",
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


class InvalidRecordException(Exception):
    """
    Custom Exception to be raised for a record
    that does not exist.
    """
    pass


class PurchaseModel:
    """
    PurchaseModel is a model for the Purchase Page.
    Carries out all data processing and database
    CRUD operations for the Purchase table.
    """

    def __init__(self, connection: sqlite3.Connection):
        """
        Constructor creates attributes that correspond to
        the Purchase table's fields and creates the
        Purchase table.

        Parameters:
            connection(object) : Sqlite3 Connection Object
        """
        self.logger = logging.getLogger(__name__)
        self.connection = connection
        self.cursor = self.connection.cursor()

        # Fields in Purchase Table
        self._id = None
        self._merchandise_id = None
        self._quantity = None
        self._total_cost = None
        self._date = None
        # self._create_purchase_table()

    @property
    def id(self) -> int | str:
        return self._id

    @id.setter
    def id(self, value: int | str):
        self._id = value

    @property
    def merchandise_id(self) -> int | str:
        return self._merchandise_id

    @merchandise_id.setter
    def merchandise_id(self, value: int | str):
        self._merchandise_id = value

    @property
    def quantity(self) -> int | str:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int | str):
        self._quantity = value

    @property
    def total_cost(self) -> float | str:
        return self._total_cost

    @total_cost.setter
    def total_cost(self, value: float | str):
        self._total_cost = value

    @property
    def date(self) -> str:
        return self._date

    @date.setter
    def date(self, value: str):
        self._date = value

    def create_purchase_table(self):
        """
        Creates Purchase table in sqlite database.
        """
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Purchase(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Merchandise_ID INTEGER,
                Quantity INTEGER,
                Total_Cost FLOAT,
                Date DATETIME,
                FOREIGN KEY (Merchandise_ID) REFERENCES Merchandise(ID));""")
            self.connection.commit()
            self.logger.info("Successfully created Purchase Table")
        except sqlite3.Error as err:
            self.logger.exception(err)

    def delete_purchase_table(self):
        """
        Deletes Purchase table when clear DB.
        """
        self.cursor.execute("""DROP TABLE Purchase;""")
        self.connection.commit()

    # Create, Delete, Read operations
    def create_record(self):
        """
        Creates record in Purchase table using attribute values
        that correspond to Purchase table fields. Then resets attribute values
        so ready for next operation.
        """
        try:
            self.cursor.execute("""INSERT INTO Purchase
                                VALUES(null, ?, ?, ?, ?)""", (
                                        self.merchandise_id,
                                        self.quantity,
                                        self.total_cost,
                                        self.date))
            self.connection.commit()
            self.logger.info("Successfully created record in Purchase Table")
        except sqlite3.IntegrityError:
            self.logger.exception(
                "Adding an entry that already exists in Purchase Table")
        finally:
            self.merchandise_id = None
            self.quantity = None
            self.total_cost = None
            self.date = None

    def delete_record(self):
        """
        Deletes record from Purchase table using id attribute.
        First checks if record to delete actually exists.
        """
        id_exists: bool = self._check_if_id_exists()

        if not id_exists:
            try:
                raise InvalidRecordException
            except InvalidRecordException:
                self.logger.exception("Can't delete record that doesn't exist")
        else:
            self.cursor.execute(f"""DELETE FROM Purchase
                                    WHERE ID = {self.id};""")
            self.connection.commit()
            self.logger.info(
                f"Successfully deleted record: {self.id} from Purchase Table")

    def _check_if_id_exists(self) -> bool:
        self.cursor.execute("""
                            SELECT ID FROM Purchase;""")
        records = self.cursor.fetchall()
        for id in records:
            if str(id[0]) == self.id:
                return True
        return False

    def retrieve_all_records(self) -> list[tuple]:
        """
        Returns all records in Purchase table

        Returns:
            list[tuple] : records
        """

        self.cursor.execute("""
                            SELECT * from Purchase;""")
        records = self.cursor.fetchall()
        return records

    def retrieve_all_ids(self) -> list[tuple]:
        """
        Returns all IDs in Purchase table

        Returns:
            list[tuple] : ids
        """
        self.cursor.execute("""SELECT ID FROM Purchase;""")
        ids = self.cursor.fetchall()
        return ids

    def retrieve_quantity(self) -> int:
        """
        Returns the quantity in a particular purchase

        Returns:
            int : quantity
        """
        self.cursor.execute(f""" SELECT Quantity
                                 FROM Purchase
                                 WHERE ID = {self.id};""")
        self.quantity = self.cursor.fetchall()[0][0]
        return self.quantity

    def retrieve_merch_id(self) -> int:
        """
        Returns merch_id for a purchase

        Returns:
            int : merchandise_id
        """
        self.cursor.execute(f"""SELECT Merchandise_ID
                                FROM Purchase
                                WHERE ID = {self.id};""")
        self.merchandise_id = self.cursor.fetchall()[0][0]
        return self.merchandise_id

    def calculate_new_quantity(self, old_quantity: int) -> int:
        """
        Method used to calculate the new quantity for a product
        type after a purchase has been made

        Parameters:
            old_quantity (int) : The current quantity of the product type

        Returns:
            int : new_total
        """
        new_total = old_quantity - int(self.quantity)
        return new_total

    def calculate_cost_and_date(self, price) -> tuple[str, str]:
        """
        Method that calculates the total price of the purchase and
        the date purchase was made.

        Parameters:
            price (float) : The price of the product type

        Returns:
            tuple[str,str] : total_cost, date_today"""
        total_cost = round(float(self.quantity) * price, 2)
        date_today = date.today()
        return str(total_cost), str(date_today)

    def calculate_sales(self) -> tuple[list[tuple], float]:
        """
        Method used for sales breakdown page to work out the
        amount to be paid to the band and phoenix by product.

        Returns:
            tuple[list[tuple], float] : results, total_cost_for_band
        """
        try:
            self.cursor.execute("""
                                SELECT Merchandise_ID,
                                SUM(Quantity),
                                ROUND(SUM(Total_Cost),2),
                                ROUND(SUM(Total_Cost) * 0.25,2),
                                ROUND(SUM(Total_Cost) * 0.75,2)
                                FROM Purchase
                                GROUP BY Merchandise_ID;""")
            results = self.cursor.fetchall()

            total_cost_for_band = 0
            for record in results:
                total_cost_for_band += record[4]
            total_cost_for_band = round(total_cost_for_band, 2)
            return results, total_cost_for_band
        except sqlite3.Error as err:
            self.logger.exception(err)
            return [], 0
