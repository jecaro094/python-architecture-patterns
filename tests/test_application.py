from fastapi.testclient import TestClient
from application import app
from serializers.input_application import OrderLineSerializer
from uuid import uuid4, UUID
from adapters.sqlite_adapter import get_db
import tests.constants as test_const
from copy import deepcopy


class SessionData:
    def all(self):
        batches_mock = test_const.BATCHES_IN_DB_MOCK_OK
        return deepcopy(batches_mock)
            
class DbMock():
    def delete(self):
        pass

    def query(self, _):
        return SessionData()

    def commit(self):
        pass

    def close(self):
        pass

async def mock_get_db():
    fake_session = DbMock() 
    try:
        yield fake_session
    finally:
        fake_session.close()


client = TestClient(app)
app.dependency_overrides[get_db] = mock_get_db

def test_allocate_ok():
    """
    Happy path for `POST allocate` endpoint
    """
    response = client.post(
        "/allocate/",
        json={
            'sku': 'SMALL-TABLE',
            'quantity': 1,
            'reference': str(uuid4())
        }
    )

    batch_reference = next(iter(test_const.BATCHES_IN_DB_MOCK_OK)).reference
    assert response.status_code == 200
    assert response.json() == {
        'message': (
            'Successfully allocated line in batch '
            f'with reference {batch_reference}'
        )
    }