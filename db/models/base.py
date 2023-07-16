from sqlalchemy.orm import declarative_base

from db.database import get_engine
from logger import get_logger

logger = get_logger(__name__)
Base = declarative_base()


def create_models():
    Base.metadata.create_all(bind=get_engine())
    logger.info("Created models")
