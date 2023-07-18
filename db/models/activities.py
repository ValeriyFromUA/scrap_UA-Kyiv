from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.models.association import company_activity_association
from db.models.base import Base


class Activity(Base):
    __tablename__ = 'activity'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    companies = relationship('Company', secondary=company_activity_association, back_populates='activities')
