from consts import LAST_PAGE, START_PAGE
from db.models.base import create_models
from scraper import (collect_data, find_all_links, open_text_file,
                     save_data_to_db, clean_trash)

if __name__ == "__main__":
    create_models()
    find_all_links(START_PAGE, LAST_PAGE)
    save_data_to_db(collect_data(open_text_file('links.txt')))
    clean_trash()
