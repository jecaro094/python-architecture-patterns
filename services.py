from adapters.repository import AbstractRepository
import model.domain as dom
from uuid import UUID, uuid4

def allocate(line: dom.OrderLine, repo: AbstractRepository) -> UUID:
    batches = repo.list()

    reference = dom.allocate(line, batches)
    repo.add(line, reference) # NOTE not a real add... just commit the session to refresh changes
    return reference


def deallocate(line: dom.OrderLine, repo: AbstractRepository) -> UUID:
    return uuid4()
