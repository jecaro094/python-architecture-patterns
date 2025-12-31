
from model.domain import OrderLine, Batch
from typing import List
from uuid import UUID, uuid4
from tests import constants as test_const
from services import allocate, deallocate
from adapters.repository import AbstractRepository
from copy import deepcopy
import constants as const
import pytest
import model.exceptions as ex
from datetime import datetime

class FakeRepoAllocateOK(AbstractRepository):
    def add(self, line: OrderLine, batch_id: UUID):
        pass
    
    def remove(self, reference: UUID) -> None:
        pass

    def list(self) -> List[Batch]:
        return [deepcopy(o) for o in test_const.BATCHES_IN_DB_MOCK_OK]


class FakeRepoDeallocateOK(AbstractRepository):

    def __init__(self, line: OrderLine):
        self.batches = [
            Batch(
                sku="SMALL-TABLE", quantity=20, eta=datetime(2024, 11, 5),
                orders={line}
            ),
        ]

    def add(self, line: OrderLine, batch_id: UUID):
        pass
    
    def remove(self, reference: UUID) -> None:
        pass

    def list(self) -> List[Batch]:
        return self.batches
    

class FakeRepoAllocateException(AbstractRepository):
    def add(self, line: OrderLine, batch_id: UUID):
        pass
    
    def get(self, reference: UUID) -> None:
        pass

    def list(self) -> List[Batch]:
        return [deepcopy(o) for o in test_const.BATCHES_IN_DB_MOCK_KO]
    
class FakeRepoDeallocateException(AbstractRepository):
    def add(self, line: OrderLine, batch_id: UUID):
        pass
    
    def remove(self, reference: UUID) -> None:
        pass

    def list(self) -> List[Batch]:
        return [deepcopy(o) for o in test_const.BATCHES_IN_DB_MOCK_OK]

# NOTE Tests allocate

def test_allocate_ok():
    """
    Allocates line in batches returned from Fake repository
    """
    line = OrderLine(reference=uuid4(), sku="SMALL-TABLE", quantity=2)
    fake_repo = FakeRepoAllocateOK()
    reference_res = allocate(line, fake_repo)

    # NOTE To me improved this check in test
    assert next(iter(test_const.BATCHES_IN_DB_MOCK_OK)).reference == reference_res

def test_allocate_exception():
    """
    Raise exception when cannot allocate in any batch from list.
    """
    line = OrderLine(reference=uuid4(), sku="SMALL-TABLE", quantity=2)
    fake_repo = FakeRepoAllocateException()

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
    line = OrderLine(reference=uuid4(), sku="SMALL-TABLE", quantity=2)
    fake_repo = FakeRepoDeallocateOK(line)
    reference_res = deallocate(line, fake_repo)

    # NOTE To be improved this check in test
    deallocated_batch = next(iter(fake_repo.batches))
    assert deallocated_batch.reference == reference_res
    assert deallocated_batch.quantity == 22


def test_allocate_exception():
    """
    Raise exception when cannot deallocate from any batch from list.
    """
    line = OrderLine(reference=uuid4(), sku="SMALL-TABLE", quantity=2)
    fake_repo = FakeRepoDeallocateException()

    with pytest.raises(ex.AllocationException) as exc_info:
        deallocate(line, fake_repo)

    assert str(exc_info.value) == const.DEALLOCATE_ERROR_MSG

    # NOTE To be improved this check in test
    assert next(iter(test_const.BATCHES_IN_DB_MOCK_OK)).quantity == 20