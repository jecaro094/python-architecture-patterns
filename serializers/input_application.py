from pydantic import BaseModel


class SerializerBase(BaseModel):
    @property
    def json(self):
        return self.__dict__
    
class OrderLineInput(SerializerBase):
    sku: str
    quantity: int
