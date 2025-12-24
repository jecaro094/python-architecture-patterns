# from unittest.mock import MagicMock, patch

from datetime import datetime

import pytest

import constants as const
import exceptions as ex
from domain import Batch, OrderLine, allocate

# NOTE Tests basic domain behaviour


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


def test_allocate_with_different_sku():
    batch = Batch(sku="SMALL-TABLE", quantity=20)
    order_line = OrderLine(sku="LARGE-TABLE", quantity=2)

    with pytest.raises(ex.AllocationException) as exc_info:
        batch.allocate(order_line)

    assert str(exc_info.value) == const.ALLOCATE_ERROR_MSG


def test_deallocate_order_line_from_batch():
    batch = Batch(sku="SMALL-TABLE", quantity=20)
    order_line = OrderLine(sku="SMALL-TABLE", quantity=2)
    batch.allocate(order_line)
    batch.deallocate(order_line)
    assert batch.quantity == 20


def test_deallocate_order_line_not_from_batch():
    batch = Batch(sku="SMALL-TABLE", quantity=20)
    order_line = OrderLine(sku="SMALL-TABLE", quantity=2)
    batch.allocate(order_line)

    with pytest.raises(ex.AllocationException) as exc_info:
        batch.deallocate(OrderLine(sku="LARGE-TABLE", quantity=2))

    assert str(exc_info.value) == const.DEALLOCATE_ERROR_MSG
    assert batch.quantity == 18


# NOTE Tests for greater than in batch


def test_batch_with_none_eta_less_than_batch_with_eta():
    """
    We check that batch with `None` has priority.
    """
    batch_with_none = Batch(sku="SMALL-TABLE", quantity=20)
    batch_date = Batch(sku="SMALL-TABLE", quantity=20, eta=datetime(2026, 11, 5))
    assert batch_with_none < batch_date


def test_batches_with_different_etas_comparaison():
    """
    We check that batch with lesser date has priority
    """
    batch_earlier = Batch(sku="SMALL-TABLE", quantity=20, eta=datetime(2026, 11, 5))
    batch_later = Batch(sku="SMALL-TABLE", quantity=20, eta=datetime(2027, 11, 5))
    assert batch_earlier < batch_later


# NOTE Tests domain function behaviour


def test_allocate_line_in_batches_minor_date():
    """
    Supposed sames SKUs in all batches, to prevent exceptions
    """
    batch_earlier = Batch(sku="SMALL-TABLE", quantity=20, eta=datetime(2026, 11, 5))
    batch_later = Batch(sku="BIG-TABLE", quantity=20, eta=datetime(2027, 11, 5))
    order_line = OrderLine(sku="SMALL-TABLE", quantity=2)

    allocation = allocate(order_line, [batch_earlier, batch_later])
    assert batch_earlier.quantity == 18
    assert batch_later.quantity == 20

    assert allocation == batch_earlier.reference


def test_allocate_line_in_batches_none_in_single_batch():
    """
    Supposed sames SKUs in all batches, to prevent exceptions
    """
    batch_date = Batch(sku="SMALL-TABLE", quantity=20, eta=datetime(2026, 11, 5))
    batch_none = Batch(sku="SMALL-TABLE", quantity=20)
    order_line = OrderLine(sku="SMALL-TABLE", quantity=2)

    allocation = allocate(order_line, [batch_date, batch_none])
    assert batch_date.quantity == 20
    assert batch_none.quantity == 18

    assert allocation == batch_none.reference


def test_allocate_line_in_batch_with_same_sku():
    batch_different_sku_earlier = Batch(
        sku="LARGE-TABLE", quantity=20, eta=datetime(2024, 11, 5)
    )
    batch_same_sku_later = Batch(
        sku="SMALL-TABLE", quantity=20, eta=datetime(2026, 11, 5)
    )
    order_line = OrderLine(sku="SMALL-TABLE", quantity=2)

    allocation = allocate(order_line, [batch_different_sku_earlier, batch_same_sku_later])
    assert batch_different_sku_earlier.quantity == 20
    assert batch_same_sku_later.quantity == 18

    assert allocation == batch_same_sku_later.reference
