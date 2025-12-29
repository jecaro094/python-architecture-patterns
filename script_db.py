from fastapi import Depends
from adapters.sqlite_adapter import batch_orders, get_db, start_mappers, create_metadata
from model.domain import Batch, OrderLine

from datetime import datetime

start_mappers()
create_metadata()

def insert_orders(lines: OrderLine, session):
    for line in lines:
        session.add(line)

def insert_batches(batches: Batch, session):
    for batches in batches:
        session.add(batches)

def delete_batches(session):
    session.query(Batch).delete()

def delete_lines(session):
    session.query(OrderLine).delete()

def delete_relations(session):
    session.query(batch_orders).delete()


def delete_from_all_tables(session):
    delete_batches(session)
    delete_lines(session)
    delete_relations(session)

lines = {
    OrderLine(sku='sku_1', quantity=5),
    OrderLine(sku='sku_2', quantity=12)
}

batches = [
    # Batch(sku='sku_1', quantity=12, orders=lines),
    Batch(sku='sku_1', quantity=12, orders=set(), eta=datetime(2026, 11, 5)),
]

session = next(get_db())

# insert_orders(lines, session)
insert_batches(batches, session)

# delete_from_all_tables(session)

session.commit()
session.close()