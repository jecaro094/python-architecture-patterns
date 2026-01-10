from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Set
from uuid import UUID, uuid4

import constants as const
import model.exceptions as ex

class OrderLine:
    def __init__(self, sku, quantity, reference):
        self.sku = sku
        self.quantity = quantity
        self.reference = reference

    def __eq__(self, other):
        if not isinstance(other, OrderLine):
            return NotImplemented
        return self.reference == other.reference

    def __hash__(self):
        return hash(self.reference)

class Batch:
    def __init__(
        self,
        sku,
        quantity,
        orders: Set[OrderLine] = set(),
        eta: Optional[date] = None,
        # reference: UUID = uuid4(),  # NOTE Danger!! if we put `reference: UUID = uuid4()` the value is fixed for all objects created!!
    ):
        self.reference = uuid4()
        self.sku = sku
        self.quantity = quantity
        self.eta = eta
        self.orders = orders

    def set_reference(self, reference: UUID):
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

        self.orders.remove(order_line)
        self.quantity += order_line.quantity

    def can_deallocate(self, order_line: OrderLine):
        return order_line.sku == self.sku and order_line in self.orders

    def can_allocate(self, order_line: OrderLine):
        return order_line.sku == self.sku and order_line not in self.orders and self.quantity >= order_line.quantity

    # NOTE Book version (more legible than mine)
    def __gt__(self, other):
        if not isinstance(other, Batch):
            return False
        if (self_eta := self.eta) is None:
            return False
        if (other_eta := other.eta) is None:
            return True

        return self_eta > other_eta


# NOTE Domain service
def allocate(line: OrderLine, batches: List[Batch]) -> UUID:
    """
    Given a list of batches in `batches`, this functions allocates the given 'line'
    in the earliest batch if possible.
    """

    # NOTE Improvement from the book
    batches_allocate_ok = (b for b in sorted(batches) if b.can_allocate(line))

    if (priority_batch := next(batches_allocate_ok, None)):
        priority_batch.allocate(order_line=line)
        return priority_batch.reference

    raise ex.AllocationException(const.ALLOCATE_ERROR_MSG)

def deallocate(line: OrderLine, batches: List[Batch]) -> UUID:
    batches_deallocate_ok = (b for b in sorted(batches) if b.can_deallocate(line))

    if (priority_batch := next(batches_deallocate_ok, None)):
        priority_batch.deallocate(order_line=line)
        return priority_batch.reference

    raise ex.AllocationException(const.DEALLOCATE_ERROR_MSG)