
from model.domain import OrderLine, Batch
from typing import List
from uuid import UUID
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

    def list(self) -> List[Batch]:
        return [deepcopy(o) for o in test_const.BATCHES_IN_DB_MOCK_OK]


class FakeRepoAllocateException(AbstractRepository):
    def __init__(self, *args, **kwargs):
        return

    def add(self, line: OrderLine, batch_id: UUID):
        pass
    
    def remove(self, reference: UUID) -> None:
        pass

    def list(self) -> List[Batch]:
        return [deepcopy(o) for o in test_const.BATCHES_IN_DB_MOCK_KO]


class FakeRepoDeallocateOK(AbstractRepository):

    def __init__(self, *args, **kwargs):
        return

    def add(self, line: OrderLine, batch_id: UUID):
        pass
    
    def remove(self, reference: UUID) -> None:
        pass

    def list(self) -> List[Batch]:
        return [deepcopy(test_const.BATCH_WITH_ALLOCATED_LINE)]
    

class FakeRepoDeallocateException(AbstractRepository):

    def __init__(self, *args, **kwargs):
        return

    def add(self, line: OrderLine, batch_id: UUID):
        pass
    
    def remove(self, reference: UUID) -> None:
        pass

    def list(self) -> List[Batch]:
        return [deepcopy(o) for o in test_const.BATCHES_IN_DB_MOCK_OK]

    