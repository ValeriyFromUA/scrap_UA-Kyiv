from typing import Dict, List

from db.database import get_session
from db.models import Activity, Company
from logger import get_logger

logger = get_logger(__name__)
session = get_session()


def save_data_to_db(data_list: List[Dict]):
    logger.info("Start: saving data to DB")
    for data in data_list:
        activities = []
        for activity_name in data['activity']:
            activity = session.query(Activity).filter_by(name=activity_name).first()
            if activity:
                activities.append(activity)
            else:
                new_activity = Activity(name=activity_name)
                activities.append(new_activity)
                session.add(new_activity)
        company = Company(
            name=data['name'],
            type=data['type'],
            address=data['address'],
            phone=', '.join(data['phones']) if data['phones'] else None,
            email=', '.join(data['emails']) if data['emails'] else None,
            url=data['url'],
            description=data['description'],
        )
        company.activities = activities
        session.add(company)

    session.commit()
    logger.info("All data was saved to DB")
