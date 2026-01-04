from pydantic import BaseModel
from uuid import UUID


class SerializerBase(BaseModel):
    @property
    def json(self):
        return self.__dict__
    
class OperationInputSerializer(SerializerBase):
    sku: str
    quantity: int
    reference: UUID


