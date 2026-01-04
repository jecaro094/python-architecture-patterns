from adapters.repository import AbstractRepository
from datetime import date
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, ForeignKey, JSON, Date, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
    registry,
    mapper,
    sessionmaker,
    relationship
)
from configuration import DB_URL
from typing import List, Optional
from sqlalchemy.pool import StaticPool
from uuid import UUID
from model.domain import OrderLine, Batch
from sqlalchemy.dialects.postgresql import UUID

# -------------------------
# Database setup
# -------------------------


metadata = MetaData()

batch_orders = Table(
    "batch_orders",
    metadata,
    Column("batch_id", UUID(as_uuid=True), ForeignKey("batches.reference")),
    Column("orderline_id", UUID(as_uuid=True), ForeignKey("order_lines.reference")),
)

order_lines = Table(
    "order_lines",
    metadata,
    Column("reference", UUID(as_uuid=True), primary_key=True),
    Column("sku", String, nullable=False),
    Column("quantity", Integer, nullable=False),
)

batches = Table(
    "batches",
    metadata,
    Column("reference", UUID(as_uuid=True), primary_key=True),
    Column("sku", String, nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

# NOTE singleton for this? Yes! In other case, a engine is created every single tyime, and
# every engine will be empty, without tables
# NOTE Singleton is handled by sqlalchemy function `create_engine`; there is no
# need to do anything...
engine = create_engine(DB_URL).execution_options(isolation_level="AUTOCOMMIT")

def create_metadata():
    metadata.create_all(engine)

def get_db():
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.close()

def start_mappers():
    mapper_registry = registry()
    mapper_registry.map_imperatively(OrderLine, order_lines)
    mapper_registry.map_imperatively(
        Batch,
        batches,
        properties={
            "orders": relationship(OrderLine, batch_orders, collection_class=set)
        }
    )

class SqliteRepo(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add(self, order_line: OrderLine, batch_id: UUID):
        self.session.commit() # NOTE uow pattern... logic to be improved?

    def remove(self, reference: UUID):
        obj = self.session.query(OrderLine).filter_by(reference=reference).first()
        self.session.delete(obj)
        self.session.commit()

    def list_batches(self) -> List[Batch]:
        return self.session.query(Batch).all()
    
    def list_order_lines(self) -> List[OrderLine]:
        return self.session.query(OrderLine).all()