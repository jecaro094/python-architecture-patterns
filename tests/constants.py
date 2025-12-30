from model.domain import Batch, OrderLine
from datetime import datetime

BATCHES_IN_DB_MOCK_OK = [
    Batch(
        sku="SMALL-TABLE", quantity=20, eta=datetime(2024, 11, 5)
    ),
    Batch(
        sku="LARGE-TABLE", quantity=20, eta=None
    ),
]

BATCHES_IN_DB_MOCK_KO = [
    Batch(
        sku="LARGE-TABLE", quantity=20, eta=datetime(2024, 11, 5)
    ),
]
