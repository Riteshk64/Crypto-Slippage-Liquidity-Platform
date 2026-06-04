import storage.db as db


async def get_spread_history(
    limit: int,
) -> list[dict]:

    rows = await db.pool.fetch(
        """
        SELECT
            timestamp,
            buy_binance_sell_kraken_bps,
            buy_kraken_sell_binance_bps
        FROM spreads
        ORDER BY timestamp DESC
        LIMIT $1
        """,
        limit,
    )

    return [
        {
            "timestamp": row["timestamp"],
            "buy_binance_sell_kraken_bps": row["buy_binance_sell_kraken_bps"],
            "buy_kraken_sell_binance_bps": row["buy_kraken_sell_binance_bps"]
        }
        for row in rows
    ]