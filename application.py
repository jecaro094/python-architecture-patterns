from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from serializers.input_application import OrderLineSerializer
import services as serv
from adapters.sqlite_adapter import SqliteRepo, get_db, create_metadata, start_mappers
from model.domain import OrderLine
from exception_handler import ExceptionMiddleware
from uuid import uuid4


app = FastAPI()

app.add_middleware(ExceptionMiddleware)

@app.on_event("startup")
def on_startup():
    start_mappers()
    create_metadata()

@app.post("/allocate")
def allocate(line: OrderLineSerializer, session = Depends(get_db)):
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
        'message': (
            'Successfully allocated line in batch '
            f'with reference {reference}'
        )
    }
    return JSONResponse(content=message)

@app.post("/deallocate")
def deallocate(line: OrderLineSerializer, session = Depends(get_db)):
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
        'message': (
            'Successfully deallocated line from batch '
            f'with reference {reference}'
        )
    }
    return JSONResponse(content=message)