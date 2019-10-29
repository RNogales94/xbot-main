from xbot.utils.product_factory import ProductFactory
from xbot.utils.product_factory_test import product_json
import pytest
from bot.message import Message


@pytest.fixture
def product(product_json):
    return ProductFactory.build_product_from_json(product_json)

def message_test(product):
    msg = Message(product)
    assert isinstance(str(msg), str)