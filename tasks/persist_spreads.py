import asyncio

import storage.db as db
from storage.state import (
    binance_orderbook,
    kraken_orderbook,
)


async def persist_spreads() -> None:
    while True:
        try:
            if (
                binance_orderbook["bids"]
                and kraken_orderbook["bids"]
            ):
                binance_bid = float(
                    binance_orderbook["bids"][0][0]
                )

                binance_ask = float(
                    binance_orderbook["asks"][0][0]
                )

                kraken_bid = float(
                    kraken_orderbook["bids"][0][0]
                )

                kraken_ask = float(
                    kraken_orderbook["asks"][0][0]
                )

                spread_bps = (
                    (kraken_bid - binance_ask)
                    / binance_ask
                ) * 10000

                await db.pool.execute(
                    """
                    INSERT INTO spreads (
                        binance_bid,
                        binance_ask,
                        kraken_bid,
                        kraken_ask,
                        spread_bps
                    )
                    VALUES ($1,$2,$3,$4,$5)
                    """,
                    binance_bid,
                    binance_ask,
                    kraken_bid,
                    kraken_ask,
                    spread_bps,
                )

        except Exception as exc:
            print(exc)

        await asyncio.sleep(1)