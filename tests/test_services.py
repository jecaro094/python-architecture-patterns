
from model.domain import OrderLine, Batch
from typing import List
from uuid import UUID
from tests import constants as test_const
from services import allocate
from adapters.repository import AbstractRepository
from copy import deepcopy
import constants as const
import pytest
import model.exceptions as ex

class FakeRepoOK(AbstractRepository):
    def add(self, line: OrderLine, batch_id: UUID):
        pass
    
    def get(self) -> None:
        pass

    def list(self) -> List[Batch]:
        return [deepcopy(o) for o in test_const.BATCHES_IN_DB_MOCK_OK]


class FakeRepoBatchesDifferentSku(AbstractRepository):
    def add(self, line: OrderLine, batch_id: UUID):
        pass
    
    def get(self) -> None:
        pass

    def list(self) -> List[Batch]:
        return [deepcopy(o) for o in test_const.BATCHES_IN_DB_MOCK_KO]
    

def test_allocate_ok():
    """
    Allocates line in batches returned from Fake repository
    """
    line = OrderLine(sku="SMALL-TABLE", quantity=2)
    fake_repo = FakeRepoOK()
    reference_res = allocate(line, fake_repo)

    # NOTE To me improved this check in test
    assert next(iter(test_const.BATCHES_IN_DB_MOCK_OK)).reference == reference_res

def test_allocate_exception():
    """
    Raise exception when cannot allocate in any batch from list.
    """
    line = OrderLine(sku="SMALL-TABLE", quantity=2)
    fake_repo = FakeRepoBatchesDifferentSku()

    with pytest.raises(ex.AllocationException) as exc_info:
        allocate(line, fake_repo)

    assert str(exc_info.value) == const.ALLOCATE_ERROR_MSG

    # NOTE To me improved this check in test
    assert next(iter(test_const.BATCHES_IN_DB_MOCK_KO)).quantity == 20
