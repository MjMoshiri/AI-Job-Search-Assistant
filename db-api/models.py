from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from datetime import datetime
Base = declarative_base()



class JobApplication(Base):
    __tablename__ = 'job_applications'

    id = Column(String, primary_key=True)
    date_added = Column(DateTime, default=datetime.now)
    description = Column(String)
    link = Column(String)
    is_qualified = Column(Boolean)
    is_not_qualified_reason = Column(String)
    has_applied = Column(Boolean)
    resume_version = Column(String)
    title = Column(String)
    company = Column(String)
    date_applied = Column(DateTime)

    def to_json(self):
        job_dict = {}
        for c in inspect(self).mapper.column_attrs:
            value = getattr(self, c.key)
            if isinstance(value, datetime):
                job_dict[c.key] = value.isoformat()
            else:
                job_dict[c.key] = value
        return job_dict