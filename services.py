from typing import List
from uuid import UUID

import model.domain as dom
from adapters.repository import AbstractRepository
from utils import transform_batch

def allocate(line: dom.OrderLine, repo: AbstractRepository) -> UUID:
    batches = repo.list_batches()

    reference = dom.allocate(line, batches)
    repo.add(
        line, reference
    )  # NOTE not a real add... just commit the session to refresh changes
    return reference


def deallocate(line: dom.OrderLine, repo: AbstractRepository) -> UUID:
    batches = repo.list_batches()
    reference = dom.deallocate(line, batches)
    repo.remove(line.reference)

    return reference


def get_batches(repo: AbstractRepository) -> List[dom.Batch]:
    batches = repo.list_batches()
    return [transform_batch(b) for b in batches]


def get_order_lines(repo: AbstractRepository) -> List[dom.OrderLine]:
    return repo.list_order_lines()
