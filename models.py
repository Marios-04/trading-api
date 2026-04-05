from sqlalchemy import Column, Integer, String, Float, DateTime 
from database import Base 
import datetime 
 
class Candle(Base): 
    __tablename__ = "candles" 
    id = Column(Integer, primary_key=True, index=True) 
    symbol = Column(String, index=True) 
    timestamp = Column(DateTime, default=datetime.datetime.utcnow) 
    open = Column(Float) 
    high = Column(Float) 
    low = Column(Float) 
    close = Column(Float) 
    volume = Column(Float) 
