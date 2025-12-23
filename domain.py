from datetime import date
from typing import Optional
from uuid import UUID, uuid4

import constants as const
import exceptions as ex


# @dataclass(frozen=True) # solo sirve si se usan atributos de clase, y no de objeto
class OrderLine:
    def __init__(self, sku, quantity, reference: UUID = uuid4()):
        self.sku = sku
        self.quantity = quantity
        self.reference = reference


class Batch:
    def __init__(
        self,
        sku,
        quantity,
        orders: set = set(),
        eta: Optional[date] = None,
        reference: UUID = uuid4(),
    ):
        self.sku = sku
        self.quantity = quantity
        self.orders = orders
        self.eta = eta
        self.reference = reference

    def __repr__(self):
        return (
            f"Batch(reference='{self.reference}', "
            f"sku='{self.sku}', quantity='{self.quantity}')"
        )

    def allocate(self, order_line: OrderLine):
        if not self.can_allocate(order_line):
            raise ex.AllocationException(const.ALLOCATE_ERROR_MSG)

        if self.quantity >= order_line.quantity:
            self.orders.add(order_line)
            self.quantity -= order_line.quantity

    def deallocate(self, order_line: OrderLine):
        if not self.can_deallocate(order_line):
            raise ex.AllocationException(const.DEALLOCATE_ERROR_MSG)

        self.orders.clear(order_line)

    def can_deallocate(self, order_line: OrderLine):
        return order_line in self.orders

    def can_allocate(self, order_line: OrderLine):
        return order_line.sku == self.sku and order_line not in self.orders
