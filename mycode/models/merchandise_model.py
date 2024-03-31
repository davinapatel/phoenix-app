import sqlite3
import logging


logging.basicConfig(filename="debug.log",
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


class InvalidRecordException(Exception):
    """ Custom Exception for when a record does not exist"""
    pass


class MerchandiseModel:

    """
    MerchandiseModel performs all data processing and
    CRUD Database Operations for the Merchandise Page
    and Merchandise Table in the Database.
    """

    def __init__(self, connection: sqlite3.Connection):

        """
        Constructor creates attributes that correspond to
        the Merchandise table's fields and creates the
        Merchandise table.

        Parameters:
            connection(object) : Sqlite3 Connection Object
        """
        self.logger = logging.getLogger(__name__)
        self.connection = connection
        self.cursor = self.connection.cursor()

        # Fields in Merchandise Table
        self._id = None
        self._product_type = None
        self._description = None
        self._price = None
        self._quantity = None
        # self._create_merchandise_table()
        # self._insert_initial_merchandise()

    @property
    def id(self) -> str | int:
        return self._id

    @id.setter
    def id(self, value: str | int):
        self._id = value

    @property
    def product_type(self) -> str:
        return self._product_type

    @product_type.setter
    def product_type(self, value: str):
        self._product_type = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def price(self) -> str | float:
        return self._price

    @price.setter
    def price(self, value: str | float):
        self._price = value

    @property
    def quantity(self) -> str | int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: str | int):
        self._quantity = value

    def create_merchandise_table(self):
        """
        Creates Merchandise table in sqlite database.
        """
        try:
            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Merchandise(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    Product_Type VARCHAR(100) UNIQUE,
                                    Description VARCHAR(255),
                                    Price FLOAT,
                                    Quantity INTEGER); """
                                )
            self.connection.commit()
            self.logger.info("Successfully created Merchandise Table")
        except sqlite3.Error as err:
            self.logger.exception(err)

    def insert_initial_merchandise(self, data):
        """
        Inserts 3 intial records into Merchandise table
        so the Merchandise table already has some products
        when application is first started.
        """
        try:
            self.cursor.executemany("""
                                    INSERT INTO Merchandise
                                    VALUES(null, ?, ?, ?, ?)""",
                                    data)
            self.connection.commit()
        except sqlite3.IntegrityError:
            self.logger.exception("Entry already exists in Merchandise Table")

    def delete_merchandise_table(self):
        """
        Deletes Merchandise Table when user wants to clear DB.
        """
        self.cursor.execute("""DROP TABLE Merchandise;""")
        self.connection.commit()

    # CRUD operations
    def add_record(self):
        """
        Uses the models attributes to add a new record to
        the Merchandise table and then resets the attribute
        values so it's ready to for the next operation.
        """
        try:
            float(self.price)
            int(self.quantity)
            self.cursor.execute("""INSERT INTO Merchandise
                                VALUES(null, ?, ?, ?, ?)""",
                                (self.product_type,
                                 self.description,
                                 self.price,
                                 self.quantity))
            self.connection.commit()
            self.logger.info("Added record to Merchandise table")
        except sqlite3.IntegrityError:
            self.logger.exception(
                "Adding an entry that already exists into Merchandise Table")
        except ValueError:
            self.logger.exception("""
                Invalid data entered to create record in merchandise table""")
        finally:
            self.id = None
            self.product_type = None
            self.description = None
            self.price = None
            self.quantity = None

    def retrieve_all_records(self) -> list[tuple]:
        """
        Returns all the records in the Merchandise Table

        Returns:
            List[tuple] : records """
        try:
            self.cursor.execute("""
                                SELECT * from Merchandise;""")
        except sqlite3.Error as err:
            self.logger.exception(err)

        records = self.cursor.fetchall()
        return records

    def delete_record(self):
        """
        Deletes record from Merchandise table using the id
        attribute. First checks whether record exists before
        performing delete operation.
        """
        id_exists: bool = self._check_if_id_exists()
        if not id_exists:
            try:
                raise InvalidRecordException
            except InvalidRecordException:
                self.logger.exception("Can't delete non-existant record")
            finally:
                self.id = None
        else:
            try:
                self.cursor.execute("""
                                        DELETE FROM Merchandise
                                        WHERE ID = ?;""", self.id)
                self.connection.commit()
                self.logger.info("Deleted record from Merchandise table")
            except sqlite3.IntegrityError as err:
                self.logger.exception(err)
            except sqlite3.ProgrammingError:
                self.logger.exception("Invalid or no ID provided to sql query")
            finally:
                self.id = None

    def _check_if_id_exists(self) -> bool:
        self.cursor.execute("""
                            SELECT ID FROM Merchandise;""")
        records = self.cursor.fetchall()
        print(records)
        for id in records:
            print(id)
            if str(id[0]) == self.id:
                return True
        return False

    def update_record(self):
        """
        Updates record using the attribute values that correspond
        to Merchandise table fields.
        Resets the attribute values at the end so ready for next
        operation.
        """
        id_exists: bool = self._check_if_id_exists()
        if not id_exists:
            try:
                raise InvalidRecordException
            except InvalidRecordException:
                self.logger.exception("Can't update record that doesn't exist")
        else:
            try:
                int(self.quantity)
                float(self.price)
                self.cursor.execute("""
                                        UPDATE Merchandise
                                        SET Product_Type = ?,
                                            Description = ?,
                                            Price = ?,
                                            Quantity = ?
                                        WHERE ID = ?;""",
                                    (self.product_type,
                                     self.description,
                                     float(self.price),
                                     int(self.quantity),
                                     int(self.id)))
                self.connection.commit()
            except ValueError:
                self.logger.exception("""
        Updating record in merchandise table failed due to invalid data""")

        self.id = None
        self.product_type = None
        self.description = None
        self.price = None
        self.quantity = None

    # Queries

    def retrieve_all_product_types(self) -> list[tuple]:
        """
        Selects and returns all product types in Merchandise table

        Returns:
            list[tuple] : product_types
        """
        self.cursor.execute("""SELECT Product_Type FROM Merchandise;""")
        product_types = self.cursor.fetchall()
        return product_types

    def retrieve_count(self, product_type: str) -> int:
        """
        Returns the quantity for a specific product type

        Parameter:
            product_type(str) : The product type
        Returns:
            int : count """

        self.cursor.execute("""SELECT Quantity
                               FROM Merchandise
                               WHERE Product_Type = ?; """, (product_type,))
        result = self.cursor.fetchall()
        count = result[0][0]
        return count

    def retrieve_price(self, product_type: str) -> float:
        """
        Returns price for specific product type

        Parameters:
            product_type(str) : The product type

        Returns:
            float : price
        """
        self.cursor.execute("""SELECT Price
                               FROM Merchandise
                               WHERE Product_Type = ?; """, (product_type,))
        price = self.cursor.fetchall()[0][0]
        return price

    def retrieve_id(self, product_type: str) -> int:
        """
        Returns id for specific product_type

        Parameters:
            product_type(str) : The product type

        Returns:
            int : id
        """
        self.cursor.execute("""SELECT ID
                               FROM Merchandise
                               WHERE Product_Type = ?; """, (product_type,))
        id = self.cursor.fetchall()[0][0]
        return id

    def retrieve_product_type(self, id: int) -> str:
        """
        Returns product type for specific id

        Parameters:
            id(int) : The product id

        Returns:
            str : product_type
        """
        self.cursor.execute("""SELECT Product_Type
                               FROM Merchandise
                               WHERE ID = ?; """, (id,))
        product_type = self.cursor.fetchall()[0][0]
        return product_type

    def retrieve_description(self, id: int) -> str:
        """
        Returns description for specific product id

        Parameters:
            id(int) : The product id

        Returns:
            str : description
        """
        self.cursor.execute("""SELECT Description
                               FROM Merchandise
                               WHERE id = ?; """, (id,))
        description = self.cursor.fetchall()[0][0]
        return description

    def retrieve_quantity(self, product_type: str) -> int:
        """
        Returns quantity for specific product_type

        Parameters:
            product_type(str) : The product type

        Returns:
            int : quantity
        """
        self.cursor.execute("""SELECT Quantity
                               FROM Merchandise
                               WHERE Product_Type = ?; """, (product_type,))
        quantity = self.cursor.fetchall()[0][0]
        return quantity

    def update_quantity(self, product_type: str, new_quantity: int):
        """
        Method used to update the quantity of product after a purchase
        has been made or cancelled

        Parameters:
            product_type(str) : The product type to update
            new_quantity(int) : The new quantity of the product
        """
        self.cursor.execute("""
                            UPDATE Merchandise
                            SET Quantity = ?
                            WHERE Product_Type = ?;""", (new_quantity,
                                                         product_type,))
        self.connection.commit()

    def retrieve_old_quantity(self):
        """
        Method used when working out the new quantity of the product
        after a purchase has been made or cancelled.

        Sets the quantity attribute
        """
        self.cursor.execute(f""" SELECT Quantity
                                 FROM Merchandise
                                 WHERE ID = {self.id};""")
        self.quantity = self.cursor.fetchall()[0][0]

    def update_quantity_using_id(self):
        """
        Updates the quantity of a product using it's product id """

        self.cursor.execute(""" UPDATE Merchandise
                                 SET Quantity = ?
                                 WHERE ID = ?;""", (self.quantity, self.id))

        self.connection.commit()

    def increase_merch_quantity(self, id: int, quantity_to_add: int):
        """
        Method used to update quantity of a product when a purchase
        has been cancelled, so the quantity of the product needs
        to be increased again.

        Parameters:
            id(int) : The product id to update
            quantity_to_add(int) : The number to add to the existing
                                    product quantity
        """
        self.id = id
        self.retrieve_old_quantity()
        self.quantity += quantity_to_add
        self.update_quantity_using_id()


if __name__ == "__main__":
    connection = sqlite3.connect("dummy.db")
    object = MerchandiseModel(connection)
