from sqlalchemy import Column, Integer, String

from db.models.base import Base


class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    activity = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)
    url = Column(String)
    description = Column(String)
