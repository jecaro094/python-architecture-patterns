from uuid import UUID

import model.domain as dom
from adapters.repository import AbstractRepository


def allocate(line: dom.OrderLine, repo: AbstractRepository) -> UUID:
    batches = repo.list()

    reference = dom.allocate(line, batches)
    repo.add(
        line, reference
    )  # NOTE not a real add... just commit the session to refresh changes
    return reference


def deallocate(line: dom.OrderLine, repo: AbstractRepository) -> UUID:
    batches = repo.list()
    reference = dom.deallocate(line, batches)
    repo.remove(line.reference)

    return reference
