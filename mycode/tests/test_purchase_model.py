import pytest
import sqlite3
from models.purchase_model import PurchaseModel


@pytest.fixture(autouse=True)
def instance():
    connection = sqlite3.connect("test.db")
    instance = PurchaseModel(connection)
    instance.create_purchase_table()
    data = [
        (1, 30, 50.99, "2024-02-29"),
        (2, 40, 60.99, "2024-02-29")
    ]

    instance.cursor.executemany("""
                                INSERT INTO Purchase
                                VALUES(null, ?, ?, ?, ?)""",
                                data)
    instance.connection.commit()
    yield instance
    print('cleaning test')
    instance.delete_purchase_table()
    connection.close()
    del instance


def test_purchase_table_created(instance):
    table_names = instance.cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table';""").fetchall()
    assert ("Purchase",) in table_names


def test_retrieve_all_records(instance):
    records = instance.retrieve_all_records()
    assert len(records) == 2


def test_retrieve_all_ids(instance):
    ids = instance.retrieve_all_ids()
    cleaned_ids = []
    for id in ids:
        cleaned_ids.append(id[0])

    assert cleaned_ids == [1, 2]
    assert len(ids) == 2


def test_retrieve_quantity(instance):
    instance.id = 1
    quantity = instance.retrieve_quantity()
    assert quantity == 30


def test_retrieve_merch_id(instance):
    instance.id = 2
    merch_id = instance.retrieve_merch_id()
    assert merch_id == 2


def test_calculate_new_quantity(instance):
    original_quantity = 100
    instance.quantity = 30
    new_quantity = instance.calculate_new_quantity(original_quantity)

    assert new_quantity == 70


def test_calculate_cost_and_date(instance):
    instance.quantity = 5
    cost, date = instance.calculate_cost_and_date(2.50)
    assert cost == "12.5"


def test_create_record(instance):
    count_records_before = len(instance.cursor.execute(
        """ SELECT * FROM Purchase; """).fetchall()
        )
    instance.merchandise_id = 2
    instance.quantity = 40
    instance.total_cost = 56.99
    instance.date = "2024-02-29"
    instance.create_record()

    count_records_after = len(instance.cursor.execute(
        """ SELECT * FROM Purchase; """).fetchall()
        )

    assert count_records_before + 1 == count_records_after


def test_delete_record(instance):
    instance.id = '1'
    instance.delete_record()

    instance.id = '2'
    instance.delete_record()

    records = instance.retrieve_all_records()
    assert len(records) == 0


def test_cannot_delete_record_that_doesnt_exist(instance):
    instance.id = '100'
    instance.delete_record()
    num_records = len(instance.cursor.execute(
        """ SELECT * FROM Purchase; """).fetchall()
        )
    assert 2 == num_records


def test_totals_returned_after_calc_sales(instance):
    results, total_cost = instance.calculate_sales()
    assert [(1, 30, 50.99, 12.75, 38.24),
            (2, 40, 60.99, 15.25, 45.74)] == results
    assert total_cost == 83.98


def test_no_totals_returned_after_calc_sales(instance):
    instance.cursor.execute("""DELETE FROM Purchase;""")
    results, total_cost = instance.calculate_sales()
    print(results, total_cost)
    assert results == []
    assert total_cost == 0
