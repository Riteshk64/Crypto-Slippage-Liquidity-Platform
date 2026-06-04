from storage.db import get_pool

async def get_spread_stats() -> dict[str, float]:
    pool = get_pool()
    row = await pool.fetchrow(
        """
        SELECT
            AVG(spread_bps) AS avg_spread,
            MAX(spread_bps) AS max_spread,
            MIN(spread_bps) AS min_spread
        FROM spreads
        WHERE timestamp >= NOW() - INTERVAL '1 minute'
        """
    )

    return {
        "avg_spread_1m": row["avg_spread"],
        "max_spread_1m": row["max_spread"],
        "min_spread_1m": row["min_spread"],
    }