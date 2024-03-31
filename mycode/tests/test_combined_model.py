import pytest
from models.combined_model import CombinedModel
from models.merchandise_model import MerchandiseModel
from models.purchase_model import PurchaseModel
import sqlite3


@pytest.fixture
def instance():
    connection = sqlite3.connect(":memory:")
    instance = CombinedModel(connection)
    return instance


def test_merch_model_created(instance):
    assert isinstance(instance.merchandise_model, MerchandiseModel)


def test_purchase_model_created(instance):
    assert isinstance(instance.purchase_model, PurchaseModel)
