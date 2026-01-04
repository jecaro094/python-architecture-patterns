from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

import services as serv
from adapters.sqlite_adapter import SqliteRepo, create_metadata, get_db, start_mappers
from exception_handler import ExceptionMiddleware
from model.domain import OrderLine
from serializers.input_application import OrderLineSerializer

app = FastAPI()  # Supports asgi (async) instead of wsgi (django / sync)

app.add_middleware(ExceptionMiddleware)


@app.on_event("startup")
def on_startup():
    start_mappers()
    create_metadata()


@app.post("/allocate")
def allocate(line: OrderLineSerializer, session=Depends(get_db)):
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
def deallocate(line: OrderLineSerializer, session=Depends(get_db)):
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
