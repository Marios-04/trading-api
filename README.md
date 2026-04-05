# Trading Market Data API

A RESTful API for ingesting and querying OHLCV candlestick data across trading symbols, built with FastAPI and SQLite.

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## Features
- Add OHLCV candlestick data for any trading symbol (EURUSD, BTCUSD, etc.)
- Retrieve historical candles by symbol
- Get statistical aggregations: average close, highest high, lowest low, total volume
- Delete data by symbol
- Auto-generated Swagger UI documentation

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/candles` | Add a new candle |
| GET | `/candles/{symbol}` | Get candles for a symbol |
| GET | `/candles/{symbol}/stats` | Get stats for a symbol |
| DELETE | `/candles/{symbol}` | Delete all candles for a symbol |

## Run Locally
```bash
pip install fastapi uvicorn sqlalchemy pydantic
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API interactively.
