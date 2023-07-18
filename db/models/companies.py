from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.models.association import company_activity_association
from db.models.base import Base


class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)
    url = Column(String)
    description = Column(String)

    activities = relationship('Activity', secondary=company_activity_association, back_populates='companies')
