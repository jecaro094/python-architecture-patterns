from typing import List

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

import services as serv
from adapters.sqlite_adapter import SqliteRepo, create_metadata, get_db, start_mappers
from exception_handler import ExceptionMiddleware
from model.domain import Batch, OrderLine
from serializers.input_serializers import OperationInputSerializer

app = FastAPI()  # Supports asgi (async) instead of wsgi (django / sync)

app.add_middleware(ExceptionMiddleware)


@app.on_event("startup")
def on_startup():
    start_mappers()
    create_metadata()


@app.post("/allocate")
def allocate(line: OperationInputSerializer, session=Depends(get_db)):
    """
    Docstring for allocate

    :param line: Description
    :type line: OrderLineInput
    :param session: Description
    """
    repo = SqliteRepo(session)

    order_line_to_add = OrderLine(**line.json)
    reference = serv.allocate(order_line_to_add, repo)

    message = {
        "message": ("Successfully allocated line in batch " f"with reference {reference}")
    }
    return JSONResponse(content=message)


@app.post("/deallocate")
def deallocate(line: OperationInputSerializer, session=Depends(get_db)):
    """
    Docstring for allocate

    :param line: Description
    :type line: OrderLineInput
    :param session: Description
    """
    repo = SqliteRepo(session)
    order_line_to_remove = OrderLine(**line.json)
    reference = serv.deallocate(order_line_to_remove, repo)

    message = {
        "message": (
            "Successfully deallocated line from batch " f"with reference {reference}"
        )
    }
    return JSONResponse(content=message)


@app.get("/batch", response_model=None)
def batches(session=Depends(get_db)) -> List[Batch]:
    """
    Retrieves batches from database
    """
    repo = SqliteRepo(session)
    return serv.get_batches(repo)


@app.get("/order_line", response_model=None)
def order_lines(session=Depends(get_db)) -> List[OrderLine]:
    """
    Retrieves batches from database
    """
    repo = SqliteRepo(session)
    return serv.get_order_lines(repo)
