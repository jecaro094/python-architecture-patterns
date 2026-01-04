
from abc import ABC, abstractmethod
from model.domain import OrderLine, Batch
from typing import List
from uuid import UUID

class AbstractRepository(ABC):

    @abstractmethod
    def add(self, line: OrderLine, batch_id: UUID):
        ...
    
    @abstractmethod
    def remove(self, reference: UUID) -> None:
        ...

    @abstractmethod
    def list_batches(self) -> List[Batch]:
        ...

    @abstractmethod
    def list_order_lines(self) -> List[OrderLine]:
        ...