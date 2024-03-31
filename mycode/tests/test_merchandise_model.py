import pytest
import sqlite3
from models.merchandise_model import MerchandiseModel


@pytest.fixture()
def instance():
    # use an in memory database
    connection = sqlite3.connect("test2.db")
    instance = MerchandiseModel(connection)
    instance.create_merchandise_table()
    test_data = [
        ("Hat", "A test item", 6.99, 12),
        ("Jacket", "Another test item", 7.99, 13)
    ]
    instance.insert_initial_merchandise(test_data)
    yield instance
    print('cleaning test')
    instance.delete_merchandise_table()
    connection.close()
    del instance


def test_merchandise_table_created(instance):
    table_names = instance.cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table';""").fetchall()
    table_name = table_names[0][0]
    assert table_name == "Merchandise"


def test_initial_records_added(instance):
    records = instance.cursor.execute("""
                        SELECT * FROM Merchandise; """).fetchall()
    assert len(records) == 2


def test_cannot_add_duplicate_record(instance):
    num_records_at_start = len(instance.cursor.execute("""
                        SELECT * FROM Merchandise;""").fetchall())
    # Set values to try and add
    instance.product_type = "Hat"
    instance.description = "A test item"
    instance.price = 6.99
    instance.quantity = 12

    instance.add_record()
    records = instance.cursor.execute("""
                        SELECT * FROM Merchandise;""").fetchall()
    product_types = []
    for type in records:
        product_types.append(type[1])
    num_times_hat_appears = product_types.count("Hat")

    assert num_records_at_start == len(records)
    assert num_times_hat_appears == 1


def test_can_retrieve_records(instance):
    records = instance.retrieve_all_records()
    assert len(records) == 2


def test_retrieve_all_product_types(instance):
    types = instance.retrieve_all_product_types()
    assert types == [("Hat",), ("Jacket",)]


def test_retrieve_count(instance):
    count = instance.retrieve_count("Hat")
    assert count == 12


def test_retrieve_price(instance):
    price = instance.retrieve_price("Hat")
    assert price == 6.99


def test_retrieve_id(instance):
    id = instance.retrieve_id("Hat")
    assert id == 1


def test_retrieve_product_type(instance):
    type = instance.retrieve_product_type(1)
    assert type == "Hat"


def test_retrieve_description(instance):
    desc = instance.retrieve_description(1)
    assert desc == "A test item"


def test_retrieve_quantity(instance):
    quantity = instance.retrieve_quantity("Hat")
    assert quantity == 12


def test_update_quantity(instance):
    old_quantity = instance.retrieve_quantity("Hat")
    instance.update_quantity("Hat", 40)
    new_quantity = instance.retrieve_quantity("Hat")

    assert new_quantity == 40
    assert new_quantity != old_quantity


def test_update_quantity_using_id(instance):
    instance.id = 2
    instance.quantity = 100
    instance.update_quantity_using_id()

    quantity = instance.retrieve_quantity("Jacket")

    assert quantity == 100


def test_increase_merch_quantity(instance):
    instance.increase_merch_quantity(2, 10)
    quantity = instance.retrieve_quantity("Jacket")

    assert quantity == 23


def test_update_record(instance):
    instance.id = '2'
    instance.product_type = "Jacket"
    instance.description = "Another test item"
    instance.price = 7.99
    instance.quantity = 13
    old_desc = instance.retrieve_description(2)

    # Change the description
    instance.description = "A new description"
    instance.update_record()

    instance.id = '2'
    new_desc = instance.retrieve_description(2)

    assert old_desc != new_desc
    assert new_desc == "A new description"


def test_add_one_record(instance):
    num_records_before = len(instance.cursor.execute("""
                        SELECT * FROM Merchandise; """).fetchall())
    instance.product_type = "test"
    instance.description = "test description"
    instance.price = "1.99"
    instance.quantity = 1

    instance.add_record()

    records = instance.cursor.execute("""
                        SELECT * FROM Merchandise; """).fetchall()

    num_records_after = len(records)

    assert num_records_before + 1 == num_records_after


def test_delete_record(instance):
    num_records_before = len(instance.cursor.execute("""
                        SELECT * FROM Merchandise; """).fetchall())
    instance.id = '1'
    instance.delete_record()
    num_records_after = len(instance.cursor.execute("""
                        SELECT * FROM Merchandise; """).fetchall())
    assert num_records_before == num_records_after + 1


def test_delete_record_failed(instance):
    num_records_before = len(instance.cursor.execute("""
                        SELECT * FROM Merchandise; """).fetchall())
    instance.id = '100'
    instance.delete_record()

    num_records_after = len(instance.cursor.execute("""
                        SELECT * FROM Merchandise; """).fetchall())

    assert num_records_before == num_records_after
