from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional
import datetime
from database import engine, get_db, Base
from models import Candle

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Trading Market Data API")

class CandleCreate(BaseModel):
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    timestamp: Optional[datetime.datetime] = None

@app.get("/")
def root():
    return {"message": "Trading Market Data API is running"}

@app.post("/candles", status_code=201)
def add_candle(candle: CandleCreate, db: Session = Depends(get_db)):
    db_candle = Candle(
        symbol=candle.symbol.upper(),
        open=candle.open,
        high=candle.high,
        low=candle.low,
        close=candle.close,
        volume=candle.volume,
        timestamp=candle.timestamp or datetime.datetime.utcnow()
    )
    db.add(db_candle)
    db.commit()
    db.refresh(db_candle)
    return db_candle

@app.get("/candles/{symbol}")
def get_candles(symbol: str, limit: int = 50, db: Session = Depends(get_db)):
    candles = db.query(Candle).filter(Candle.symbol == symbol.upper()).order_by(Candle.timestamp.desc()).limit(limit).all()
    if not candles:
        raise HTTPException(status_code=404, detail=f"No data found for {symbol}")
    return candles

@app.get("/candles/{symbol}/stats")
def get_stats(symbol: str, db: Session = Depends(get_db)):
    result = db.query(
        func.avg(Candle.close).label("avg_close"),
        func.max(Candle.high).label("highest_high"),
        func.min(Candle.low).label("lowest_low"),
        func.sum(Candle.volume).label("total_volume"),
        func.count(Candle.id).label("candle_count")
    ).filter(Candle.symbol == symbol.upper()).first()
    if not result.candle_count:
        raise HTTPException(status_code=404, detail=f"No data found for {symbol}")
    return {
        "symbol": symbol.upper(),
        "avg_close": round(result.avg_close, 5),
        "highest_high": result.highest_high,
        "lowest_low": result.lowest_low,
        "total_volume": result.total_volume,
        "candle_count": result.candle_count
    }

@app.delete("/candles/{symbol}")
def delete_symbol(symbol: str, db: Session = Depends(get_db)):
    deleted = db.query(Candle).filter(Candle.symbol == symbol.upper()).delete()
    db.commit()
    if not deleted:
        raise HTTPException(status_code=404, detail=f"No data found for {symbol}")
    return {"message": f"Deleted {deleted} candles for {symbol.upper()}"}