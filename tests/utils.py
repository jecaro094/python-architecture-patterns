
from model.domain import OrderLine, Batch
from typing import List
from uuid import UUID, uuid4
from tests import constants as test_const
from adapters.repository import AbstractRepository
from copy import deepcopy


class FakeRepoAllocateOK(AbstractRepository):

    def __init__(self, *args, **kwargs):
        return

    def add(self, line: OrderLine, batch_id: UUID):
        pass
    
    def remove(self, reference: UUID) -> None:
        pass

    def list_batches(self) -> List[Batch]:
        return [deepcopy(o) for o in test_const.BATCHES_IN_DB_MOCK_OK]
    
    def list_order_lines(self):
        # NOTE Provisional logic; to be adapted to the test(s)
        return [OrderLine(sku='', quantity=1, reference=uuid4())]


class FakeRepoAllocateException(AbstractRepository):
    def __init__(self, *args, **kwargs):
        return

    def add(self, line: OrderLine, batch_id: UUID):
        pass
    
    def remove(self, reference: UUID) -> None:
        pass

    def list_batches(self) -> List[Batch]:
        return [deepcopy(o) for o in test_const.BATCHES_IN_DB_MOCK_KO]
    
    def list_order_lines(self):
        # NOTE Provisional logic; to be adapted to the test(s)
        return [OrderLine(sku='', quantity=1, reference=uuid4())]


class FakeRepoDeallocateOK(AbstractRepository):

    def __init__(self, *args, **kwargs):
        return

    def add(self, line: OrderLine, batch_id: UUID):
        pass
    
    def remove(self, reference: UUID) -> None:
        pass

    def list_batches(self) -> List[Batch]:
        return [deepcopy(test_const.BATCH_WITH_ALLOCATED_LINE)]
    
    def list_order_lines(self):
        # NOTE Provisional logic; to be adapted to the test(s)
        return [OrderLine(sku='', quantity=1, reference=uuid4())]
    

class FakeRepoDeallocateException(AbstractRepository):

    def __init__(self, *args, **kwargs):
        return

    def add(self, line: OrderLine, batch_id: UUID):
        pass
    
    def remove(self, reference: UUID) -> None:
        pass

    def list_batches(self) -> List[Batch]:
        return [deepcopy(o) for o in test_const.BATCHES_IN_DB_MOCK_OK]
    
    def list_order_lines(self):
        # NOTE Provisional logic; to be adapted to the test(s)
        return [OrderLine(sku='', quantity=1, reference=uuid4())]

    