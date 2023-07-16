from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy_utils import create_database, database_exists

from consts import DB_URL
from logger import get_logger

logger = get_logger(__name__)


def get_engine(url: str = DB_URL) -> Engine:
    if not database_exists(url):
        create_database(url)
        logger.info(f'Database not exist, creating new db {url}')
    engine = create_engine(url)
    logger.info(f'start engine: {url}')
    return engine


def get_session() -> Session:
    Session = sessionmaker(bind=get_engine())
    return Session()
