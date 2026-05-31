import asyncio

from fastapi import FastAPI

from analytics.slippage import estimate_buy_slippage
from ingestion.binance import stream
from storage.state import orderbook

app: FastAPI = FastAPI()

@app.on_event("startup")
async def startup() -> None:
    asyncio.create_task(stream())

@app.get("/orderbook")
def get_orderbook() -> dict[str, str] | dict[str, str]:
    if not orderbook["bids"]:
        return {"status": "no data"}

    return {
        "best_bid": orderbook["bids"][0][0],
        "best_ask": orderbook["asks"][0][0],
    }

@app.get("/slippage/{usd_size}")
def get_slippage(usd_size: float) -> dict:
    return estimate_buy_slippage(orderbook, usd_size)