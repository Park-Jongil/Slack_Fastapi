from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TeamData(Base):
    __tablename__ = "team_data"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String)
    name = Column(String)
    status = Column(String)
    date = Column(String)

class SalesData(Base):
    __tablename__ = "sales_data"
    id = Column(Integer, primary_key=True)
    team_id = Column(String)
    name = Column(String)
    status = Column(String)
    date = Column(String)

class SlackMessage(Base):
    __tablename__ = "SlackMessage"
    id = Column(Integer, primary_key=True)
    Alarm = Column(String)
    Region = Column(String)
    NodeName = Column(String)
    DateTime = Column(DateTime)
    Status = Column(String)
