from sqlalchemy import Column, Integer, String, Float, DateTime, func
from database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String(45), index=True)
    city = Column(String)
    region = Column(String)
    country = Column(String)
    postal = Column(String, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String, nullable=True)
    isp = Column(String, nullable=True)
    org = Column(String, nullable=True)
    hostname = Column(String, nullable=True)
    device = Column(String, nullable=True)
    os = Column(String, nullable=True)
    browser = Column(String, nullable=True)
    screen_size = Column(String, nullable=True)
    timestamp = Column(DateTime, default=func.now())  # 取得時刻
