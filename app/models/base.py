import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TimestampMixin:
    created_at=Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at=Column(DateTime, default=datetime.datetime.now, nullable=False)