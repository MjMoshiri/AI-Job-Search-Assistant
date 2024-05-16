from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JobApplication(Base):
    __tablename__ = 'job_applications'

    id = Column(String, primary_key=True)
    date_added = Column(DateTime)
    description = Column(String)
    website = Column(String)
    is_qualified = Column(Boolean)
    is_not_qualified_reason = Column(String)
    is_a_match = Column(Boolean)
    has_applied = Column(Boolean)
    resume_version = Column(String)
    title = Column(String)
    company = Column(String)
    date_applied = Column(DateTime)