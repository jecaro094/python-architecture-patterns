from adapters.repository import AbstractRepository
import model.domain as dom
from uuid import UUID

def allocate(line: dom.OrderLine, repo: AbstractRepository):
    batches = repo.list()
    reference = dom.allocate(line, batches)

    repo.add(line, reference)
    # If domain allocation works, update batches, and add order line

    print(f'batches: {batches}')