
from abc import ABC, abstractmethod
from model.domain import OrderLine, Batch
from typing import List

class AbstractRepository(ABC):

    @abstractmethod
    def add(self, line: OrderLine):
        ...
    
    @abstractmethod
    def get(self) -> None:
        ...

    @abstractmethod
    def list(self) -> List[Batch]:
        ...