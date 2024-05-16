from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, JobApplication
import os


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.create_all(engine)


def add_job_application(job_details):
    session = Session()
    job_application = JobApplication(**job_details)
    session.add(job_application)
    session.commit()
    session.close()

