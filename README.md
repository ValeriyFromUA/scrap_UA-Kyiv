![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

# Description

This application collects data about companies operating in Kyiv from the website ua-region.com.ua and stores it in a
PostgreSQL database (the default settings will result in approximately 16,200 entries). The following fields are
included in the database:

- Company name
- Company type (Internet shop, LLC, veterinary clinic, etc.)
- Areas of activity
- Address
- Phone numbers
- Email addresses
- Website
- Short description

## Usage

To use the application, follow these steps:

1. Clone the code using `git clone ...` or download it as a zip archive.
2. Create a `.env` file based on the `env_example` file and enter your own data.
3. Set the `START_PAGE` and `LAST_PAGE` values in `create_db_with_data.py` to specify the range of pages to search. Make
   sure the specified pages exist on the website https://www.ua-region.com.ua/ter/8000000.
4. Run `create_db_with_data.py` and wait for the results. Depending on the number of links, this process may take some
   time. The current progress will be displayed in the logs.

Important:
The program creates a temporary file called `links.txt` to store the links to company pages. It will be deleted after
the data is entered into the database.
If you need to keep this file, delete or comment out the `clean_trash()` function in `create_db_with_data.py`.

A bit more about `create_db_with_data.py`:

- `create_models()` - creates the database and models.
- `find_all_links(START_PAGE, LAST_PAGE)` - searches for all links to company pages and saves them in `links.txt`.
- `save_data_to_db(collect_data(open_text_file('links.txt')))` - processes the pages, retrieves the data, and saves it
  to the database.
- `clean_trash()` - deletes temporary files.

If needed, the functions can be used separately.
To search for companies in a different region, modify the URL in `scraper.py` (it's straightforward).