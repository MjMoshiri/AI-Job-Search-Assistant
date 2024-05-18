from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, JobApplication
import os


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.create_all(engine)



def add(job_details):
    session = Session()
    try:
        job_application = JobApplication(**job_details)
        session.add(job_application)
        session.commit()
        return True
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()

def update(job_id, job_details):
    session = Session()
    try:
        job_application = session.query(JobApplication).filter(JobApplication.id == job_id).first()
        if job_application:
            for key, value in job_details.items():
                setattr(job_application, key, value)
            session.commit()
            return True
        else:
            return False
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()
        
def check_if_id_exists(id):
    session = Session()
    try:
        existing_application = session.query(JobApplication).filter(JobApplication.id == id).first()
        return existing_application is not None
    finally:
        session.close()
        
def get_recent(n):
    session = Session()
    try:
        job_applications = session.query(JobApplication).order_by(JobApplication.date_added.desc()).limit(n).all()
        return job_applications
    except Exception:
        return None
    finally:
        session.close()
        
def get_unprocessed(n):
    session = Session()
    try:
        job_applications = session.query(JobApplication).filter(JobApplication.is_qualified == None).limit(n).all()
        return job_applications
    except Exception:
        return None
    finally:
        session.close()

