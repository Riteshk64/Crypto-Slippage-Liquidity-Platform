# Crypto Liquidity Analytics

## Features
- Real-time order book ingestion
- Cross-exchange spread monitoring
- Slippage estimation
- Historical storage with PostgreSQL/TimescaleDB
- FastAPI REST API

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- WebSockets
- Next.js

## Setup

pip install -r requirements.txt

## Run

uvicorn main:app --reload

## API Endpoints

GET /spread
GET /slippage
GET /orderbook

## Deployment

Hosted on Render