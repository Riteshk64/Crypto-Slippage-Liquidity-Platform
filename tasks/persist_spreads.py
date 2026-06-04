import asyncio
import logging

import storage.db as db
from storage.state import (
    binance_orderbook,
    kraken_orderbook,
)
from analytics.spread import calculate_spread

logger = logging.getLogger(__name__)

async def persist_spreads() -> None:
    while True:
        try:
            if (
                binance_orderbook["bids"]
                and kraken_orderbook["bids"]
            ):
                spread = calculate_spread(
                    binance_orderbook,
                    kraken_orderbook,
                )

                await db.pool.execute(
                    """
                    INSERT INTO spreads (
                        binance_bid,
                        binance_ask,
                        kraken_bid,
                        kraken_ask,
                        buy_binance_sell_kraken_bps,
                        buy_kraken_sell_binance_bps
                    )
                    VALUES ($1,$2,$3,$4,$5,$6)
                    """,
                    spread["binance_bid"],
                    spread["binance_ask"],
                    spread["kraken_bid"],
                    spread["kraken_ask"],
                    spread["buy_binance_sell_kraken_bps"],
                    spread["buy_kraken_sell_binance_bps"],
                )

        except Exception as exc:
            logger.exception(exc)

        await asyncio.sleep(1)