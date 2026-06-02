import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI,HTTPException

from analytics.slippage import estimate_buy_slippage
from ingestion.binance import stream as binance_stream
from ingestion.kraken import stream as kraken_stream
from storage.state import (binance_orderbook,kraken_orderbook,)
from storage.db import connect_db, close_db
from tasks.persist_spreads import persist_spreads
import storage.db as db
from analytics.spread_stats import get_spread_stats
from tasks.persist_slippage import persist_slippage
from analytics.slippage_history import get_slippage_history
from analytics.spread import calculate_spread

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()

    asyncio.create_task(binance_stream())
    asyncio.create_task(kraken_stream())
    asyncio.create_task(persist_spreads())
    asyncio.create_task(persist_slippage())

    yield

    await close_db()


app: FastAPI = FastAPI(lifespan=lifespan)


@app.get("/binance/orderbook")
def get_binance_orderbook() -> dict[str, str]:
    if not binance_orderbook["bids"]:
        return {"status": "no data"}

    return {
        "best_bid": binance_orderbook["bids"][0][0],
        "best_ask": binance_orderbook["asks"][0][0],
    }

@app.get("/kraken/orderbook")
def get_kraken_orderbook() -> dict[str, str]:
    if not kraken_orderbook["bids"]:
        return {"status": "no data"}

    return {
        "best_bid": kraken_orderbook["bids"][0][0],
        "best_ask": kraken_orderbook["asks"][0][0],
    }


@app.get("/slippage/{exchange}/{usd_size}")
def get_slippage(
    exchange: str,
    usd_size: float,
) -> dict[str, float]:

    if usd_size <= 0:
        raise HTTPException(
            status_code=400,
            detail="usd_size must be positive",
        )

    if exchange == "binance":
        orderbook = binance_orderbook

    elif exchange == "kraken":
        orderbook = kraken_orderbook

    else:
        raise HTTPException(
            status_code=400,
            detail="invalid exchange",
        )

    try:
        return estimate_buy_slippage(
            orderbook=orderbook,
            usd_size=usd_size,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    
@app.get("/spread")
def get_spread() -> dict[str, float]:

    if (
        not binance_orderbook["bids"]
        or not kraken_orderbook["bids"]
    ):
        raise HTTPException(
            status_code=400,
            detail="orderbook data unavailable",
        )


    return calculate_spread(
        binance_orderbook,
        kraken_orderbook,
    )

@app.get("/spread/history")
async def get_spread_history(limit: int = 100,):

    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 1000",
        )

    rows = await db.pool.fetch(
        """
        SELECT
            timestamp,
            spread_bps
        FROM spreads
        ORDER BY timestamp DESC
        LIMIT $1
        """,
        limit,
    )

    return [
        {
            "timestamp": row["timestamp"],
            "spread_bps": row["spread_bps"],
        }
        for row in rows
    ]

@app.get("/spread/stats")
async def spread_stats() -> dict[str, float]:
    return await get_spread_stats()

@app.get("/slippage-history/{exchange}")
async def slippage_history(
    exchange: str,
    limit: int = 100,
):
    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 1000",
        )

    if exchange not in (
        "binance",
        "kraken",
    ):
        raise HTTPException(
            status_code=400,
            detail="invalid exchange",
        )

    return await get_slippage_history(
        exchange,
        limit,
    )