import pytest
from controllers.controller_main import Controller
from models.combined_model import CombinedModel
from controllers.home_controller import HomeController
from controllers.merchandise_controller import MerchandiseController
from controllers.purchase_controller import PurchaseController
from controllers.sales_breakdown_controller import SalesController


@pytest.fixture()
def instance():
    instance = Controller(":memory:")
    return instance


def test_combined_model_created(instance):
    assert isinstance(instance.combined_model, CombinedModel)


def test_home_controller_created(instance):
    assert isinstance(instance.home_controller, HomeController)


def test_merchandise_controlled_created(instance):
    assert isinstance(instance.merchandise_controller, MerchandiseController)


def test_purchase_controller_created(instance):
    assert isinstance(instance.purchase_controller, PurchaseController)


def test_sales_controller_created(instance):
    assert isinstance(instance.sales_controller, SalesController)
