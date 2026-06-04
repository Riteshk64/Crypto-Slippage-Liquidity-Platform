from storage.db import get_pool


async def get_slippage_history(
    exchange: str,
    limit: int,
) -> list[dict]:

    pool = get_pool()
    rows = await pool.fetch(
        """
        SELECT
            timestamp,
            slippage_10k,
            slippage_50k,
            slippage_100k
        FROM slippage_snapshots
        WHERE exchange = $1
        ORDER BY timestamp DESC
        LIMIT $2
        """,
        exchange,
        limit,
    )

    return [
        {
            "timestamp": row["timestamp"],
            "slippage_10k": row["slippage_10k"],
            "slippage_50k": row["slippage_50k"],
            "slippage_100k": row["slippage_100k"],
        }
        for row in rows
    ]