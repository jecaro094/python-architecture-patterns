from fastapi.testclient import TestClient
from application import app
from adapters.sqlite_adapter import get_db
import tests.constants as test_const
from unittest.mock import patch
import tests.utils as test_utils
import tests.constants as test_const

async def mock_get_db():
    return None

# Fastapi client setup
client = TestClient(app)
app.dependency_overrides[get_db] = mock_get_db


@patch('application.SqliteRepo', test_utils.FakeRepoAllocateOK)
def test_allocate_200():
    """
    Happy path for `POST allocate` endpoint
    """
    response = client.post(
        "/allocate/",
        json=test_const.ORDER_LINE_JSON_DATA
    )

    batch_reference = next(iter(test_const.BATCHES_IN_DB_MOCK_OK)).reference
    assert response.status_code == 200
    assert response.json() == {
        'message': (
            'Successfully allocated line in batch '
            f'with reference {batch_reference}'
        )
    }


@patch('application.SqliteRepo', test_utils.FakeRepoAllocateException)
def test_allocate_400():
    """
    A case in which we cannot allocate
    """
    response = client.post(
        "/allocate/",
        json=test_const.ORDER_LINE_JSON_DATA
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot allocate"}


@patch('application.SqliteRepo', test_utils.FakeRepoDeallocateOK)
def test_deallocate_200():
    """
    Happy path for `POST allocate` endpoint
    """
    response = client.post(
        "/deallocate/",
        json=test_const.ORDER_LINE_JSON_DATA
    )

    batch_reference = test_const.BATCH_WITH_ALLOCATED_LINE.reference
    assert response.status_code == 200
    assert response.json() == {
        'message': (
            'Successfully deallocated line from batch '
            f'with reference {batch_reference}'
        )
    }

@patch('application.SqliteRepo', test_utils.FakeRepoDeallocateException)
def test_deallocate_400():
    """
    A case in which we cannot deallocate
    """
    response = client.post(
        "/deallocate/",
        json=test_const.ORDER_LINE_JSON_DATA
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot deallocate"}