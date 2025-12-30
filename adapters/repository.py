
from abc import ABC, abstractmethod
from model.domain import OrderLine, Batch
from typing import List
from uuid import UUID

class AbstractRepository(ABC):

    @abstractmethod
    def add(self, line: OrderLine, batch_id: UUID):
        ...
    
    @abstractmethod
    def get(self) -> None:
        ...

    @abstractmethod
    def list(self) -> List[Batch]:
        ...