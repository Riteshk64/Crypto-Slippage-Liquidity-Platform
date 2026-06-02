import asyncio

import storage.db as db

from analytics.slippage import (
    estimate_buy_slippage,
)

from storage.state import (
    binance_orderbook,
    kraken_orderbook,
)


async def persist_slippage() -> None:
    while True:
        try:
            exchanges = {
                "binance": binance_orderbook,
                "kraken": kraken_orderbook,
            }

            for name, orderbook in exchanges.items():

                if not orderbook["asks"]:
                    continue

                slippage_10k = estimate_buy_slippage(
                    orderbook,
                    10000,
                )["slippage_bps"]

                slippage_50k = estimate_buy_slippage(
                    orderbook,
                    50000,
                )["slippage_bps"]

                slippage_100k = estimate_buy_slippage(
                    orderbook,
                    100000,
                )["slippage_bps"]

                await db.pool.execute(
                    """
                    INSERT INTO slippage_snapshots (
                        exchange,
                        slippage_10k,
                        slippage_50k,
                        slippage_100k
                    )
                    VALUES ($1,$2,$3,$4)
                    """,
                    name,
                    slippage_10k,
                    slippage_50k,
                    slippage_100k,
                )

        except Exception as exc:
            print(exc)

        await asyncio.sleep(1)