from typing import Any


def calculate_liquidity(
    orderbook: dict[str, Any],
) -> dict[str, float]:

    bid_depth_usd = sum(
        float(price) * float(qty)
        for price, qty in orderbook["bids"][:10]
    )

    ask_depth_usd = sum(
        float(price) * float(qty)
        for price, qty in orderbook["asks"][:10]
    )

    return {
        "bid_depth_usd": bid_depth_usd,
        "ask_depth_usd": ask_depth_usd,
        "total_depth_usd": (
            bid_depth_usd + ask_depth_usd
        ),
    }