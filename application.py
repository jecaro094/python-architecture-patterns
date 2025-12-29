from fastapi import FastAPI, Depends
from serializers.input_application import OrderLineInput
import services as serv
from adapters.sqlite_adapter import SqliteRepo, get_db, create_metadata, start_mappers
from model.domain import OrderLine

app = FastAPI()

@app.on_event("startup")
def on_startup():
    start_mappers()
    create_metadata()

@app.post("/allocate")
def allocate(line: OrderLineInput, session = Depends(get_db)):
    """
    Docstring for allocate
    
    :param line: Description
    :type line: OrderLineInput
    :param session: Description
    """
    repo = SqliteRepo(session)
    order_line_to_add = OrderLine(**line.json)
    serv.allocate(order_line_to_add, repo)

    return {"message": "FastAPI is running"}
