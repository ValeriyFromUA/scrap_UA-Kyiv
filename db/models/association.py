from sqlalchemy import Column, Integer, ForeignKey, Table

from db.models.base import Base

company_activity_association = Table(
    'company_activity_association',
    Base.metadata,
    Column('company_id', Integer, ForeignKey('company.id')),
    Column('activity_id', Integer, ForeignKey('activity.id'))
)
