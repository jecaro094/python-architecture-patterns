from adapters.repository import AbstractRepository
import model.domain as dom
from uuid import UUID

def allocate(line: dom.OrderLine, repo: AbstractRepository):
    batches = repo.list()
    reference = dom.allocate(line, batches)
    repo.add(line, reference) # NOTE not a real add... just commit the session to refresh changes

def deallocate(line: dom.OrderLine, repo: AbstractRepository):
    pass
