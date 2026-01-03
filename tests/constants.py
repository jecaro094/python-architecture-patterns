from model.domain import Batch, OrderLine
from datetime import datetime
from uuid import uuid4

# Mock order line data for e2e tests

TEST_QUANTITY = 1
TEST_SKU = 'SMALL-TABLE'
TEST_REFERENCE = uuid4()

ORDER_LINE_JSON_DATA = {
    'sku': TEST_SKU,
    'quantity': TEST_QUANTITY,
    'reference': str(TEST_REFERENCE)
}

# Mock data from database

ALLOCATED_LINE = OrderLine(
    sku=TEST_SKU,
    quantity=TEST_QUANTITY,
    reference=TEST_REFERENCE
)

BATCH_WITH_ALLOCATED_LINE = Batch(
    sku="SMALL-TABLE", quantity=20, eta=datetime(2024, 11, 5),
    orders={ALLOCATED_LINE}
)

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
