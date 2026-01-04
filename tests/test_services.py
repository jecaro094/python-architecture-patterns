
from model.domain import OrderLine
from uuid import uuid4
from tests import constants as test_const
from services import allocate, deallocate
import constants as const
import pytest
import model.exceptions as ex
import tests.utils as test_utils

# NOTE Tests allocate

def test_allocate_ok():
    """
    Allocates line in batches returned from Fake repository
    """
    line = OrderLine(reference=uuid4(), sku="SMALL-TABLE", quantity=2)
    fake_repo = test_utils.FakeRepoAllocateOK()
    reference_res = allocate(line, fake_repo)

    # NOTE To be improved this check in test
    assert next(iter(test_const.BATCHES_IN_DB_MOCK_OK)).reference == reference_res

def test_allocate_exception():
    """
    Raise exception when cannot allocate in any batch from list.
    """
    line = OrderLine(reference=uuid4(), sku="SMALL-TABLE", quantity=2)
    fake_repo = test_utils.FakeRepoAllocateException()

    with pytest.raises(ex.AllocationException) as exc_info:
        allocate(line, fake_repo)

    assert str(exc_info.value) == const.ALLOCATE_ERROR_MSG

    # NOTE To be improved this check in test
    assert next(iter(test_const.BATCHES_IN_DB_MOCK_KO)).quantity == 20

# NOTE Tests deallocate

def test_deallocate_ok():
    """
    Deallocate line from batches returned from Fake repository
    """
    line = test_const.ALLOCATED_LINE
    fake_repo = test_utils.FakeRepoDeallocateOK()
    reference_res = deallocate(line, fake_repo)

    # NOTE To be improved this check in test
    deallocated_batch = test_const.BATCH_WITH_ALLOCATED_LINE
    assert deallocated_batch.reference == reference_res


def test_deallocate_exception():
    """
    Raise exception when cannot deallocate from any batch from list.
    """
    line = OrderLine(reference=uuid4(), sku="SMALL-TABLE", quantity=2)
    fake_repo = test_utils.FakeRepoDeallocateException()

    with pytest.raises(ex.AllocationException) as exc_info:
        deallocate(line, fake_repo)

    assert str(exc_info.value) == const.DEALLOCATE_ERROR_MSG

    # NOTE To be improved this check in test
    assert next(iter(test_const.BATCHES_IN_DB_MOCK_OK)).quantity == 20
