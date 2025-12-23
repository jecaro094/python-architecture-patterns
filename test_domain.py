# from unittest.mock import MagicMock, patch

import pytest

import constants as const
import exceptions as ex
from domain import Batch, OrderLine


def test_allocate_in_batch_order_line_greater():
    batch = Batch(sku="SMALL-TABLE", quantity=20)
    order_line = OrderLine(sku="SMALL-TABLE", quantity=2)
    batch.allocate(order_line)
    print(batch)
    assert batch.quantity == 18


def test_allocate_in_batch_order_line_equal():
    batch = Batch(sku="SMALL-TABLE", quantity=20)
    order_line = OrderLine(sku="SMALL-TABLE", quantity=20)
    batch.allocate(order_line)
    assert batch.quantity == 0


def test_allocate_in_batch_order_line_minor():
    batch = Batch(sku="SMALL-TABLE", quantity=20)
    order_line = OrderLine(sku="SMALL-TABLE", quantity=40)
    batch.allocate(order_line)
    assert batch.quantity == 20


def test_allocate_in_batch_order_line_twice():
    batch = Batch(sku="SMALL-TABLE", quantity=20)
    order_line = OrderLine(sku="SMALL-TABLE", quantity=2)
    batch.allocate(order_line)

    with pytest.raises(ex.AllocationException) as exc_info:
        batch.allocate(order_line)

    assert str(exc_info.value) == const.ALLOCATE_ERROR_MSG
    assert batch.quantity == 18


def test_allocate_different_sku():
    batch = Batch(sku="SMALL-TABLE", quantity=20)
    order_line = OrderLine(sku="LARGE-TABLE", quantity=2)

    with pytest.raises(ex.AllocationException) as exc_info:
        batch.allocate(order_line)

    assert str(exc_info.value) == const.ALLOCATE_ERROR_MSG


# TODO Deallocate to be tested...
