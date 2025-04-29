from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Tender(Base):
    __tablename__ = 'tenders'
    id = Column(Integer, primary_key=True)
    Opening_Date = Column(DateTime)
    Closing_Date = Column(DateTime)
    e_Published_Date = Column(DateTime)
    title = Column(String)
    Organisation = Column(Text)
    source_portal = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
   

class CompanyProfile(Base):
    __tablename__ = 'company_profiles'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    profile_text = Column(Text)
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)

class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('company_profiles.id'))
    tender_id = Column(Integer, ForeignKey('tenders.id'))
    match_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine('sqlite:///tender_tracker.db')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
