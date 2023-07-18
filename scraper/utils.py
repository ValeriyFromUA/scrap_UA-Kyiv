import os
from typing import List, NoReturn

from db.database import get_session
from logger import get_logger

logger = get_logger(__name__)
session = get_session()


def open_text_file(file_name: str) -> List[str]:
    with open(file_name, 'r') as file:
        lines = file.readlines()
        return lines


def clean_trash() -> NoReturn:
    if os.path.exists('links.txt'):
        os.remove('links.txt')
        logger.info("File 'links.txt' was deleted.")
    else:
        logger.info("File 'links.txt' not exist")
