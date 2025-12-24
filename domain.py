from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Set
from uuid import UUID, uuid4

import constants as const
import exceptions as ex

# @dataclass(frozen=True) # solo sirve si se usan atributos de clase, y no de objeto


# NOTE This was my first approach, which is not bad
# NOTE But this is an ENTITY and not a VALUE OBJECT (take into account...)
class OrderLine:
    def __init__(self, sku, quantity):
        self.reference = uuid4()
        self.sku = sku
        self.quantity = quantity


# NOTE This is a VALUE OBJECT: those identified uniquely by the data it holds (in its attributes)
# @dataclass(frozen=True)
# class OrderLine:
#     sku: str
#     quantity: int
#     reference: UUID # We have to provide the unique uuid4() in its instantiation

# Example: order_line = OrderLine(reference=uuid4(), sku="SMALL-TABLE", quantity=40)

# NOTE
# ENTITY: LONG LIVE IDENTITY
# VALUE OBJECT: IDENTIFIED BY ITS DATA


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
        self.orders = orders
        self.eta = eta

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
        return order_line in self.orders

    def can_allocate(self, order_line: OrderLine):
        return order_line.sku == self.sku and order_line not in self.orders

    # NOTE Mine (first version, not that bad)
    # def __gt__(self, other):
    #     if not isinstance(other, Batch):
    #         return False
    #     if self_eta := self.eta :
    #         return self_eta > other_eta if (other_eta := other.eta) else True
    #     return False

    # NOTE Book version (more legible than mine)
    def __gt__(self, other):
        if not isinstance(other, Batch):
            return False
        if (self_eta := self.eta) is None:
            return False
        if (other_eta := other.eta) is None:
            return True

        return self_eta > other_eta


def allocate(line: OrderLine, batches: List[Batch]) -> UUID:
    """
    Given a list of batches in `batches`, this functions allocates the given 'line'
    in the earliest batch if possible.
    """

    # NOTE Mine (could improve)
    # ordered_batches: List[Batch] = sorted(batches)
    # priority_batch = next(iter(ordered_batches))

    # NOTE Improvement from the book
    priority_batch = next(b for b in sorted(batches) if b.can_allocate(line))

    priority_batch.allocate(order_line=line)
    return priority_batch.reference
