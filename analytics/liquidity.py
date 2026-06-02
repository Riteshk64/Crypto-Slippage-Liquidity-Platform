from typing import Any


def calculate_depth(
    orderbook: dict[str, Any],
) -> dict[str, float]:

    best_ask = float(
        orderbook["asks"][0][0]
    )

    levels = {
        10: 0.0,
        25: 0.0,
        50: 0.0,
    }

    for price, qty in orderbook["asks"]:
        price = float(price)
        qty = float(qty)

        move_bps = (
            (price - best_ask)
            / best_ask
        ) * 10000

        usd_value = price * qty

        if move_bps <= 10:
            levels[10] += usd_value

        if move_bps <= 25:
            levels[25] += usd_value

        if move_bps <= 50:
            levels[50] += usd_value

    return {
        # "usd_depth_10bps": levels[10],
        # "usd_depth_25bps": levels[25],
        # "usd_depth_50bps": levels[50],
        "best_ask": best_ask,
        "last_ask": float(orderbook["asks"][-1][0]),
        "usd_depth_10bps": levels[10],
        "usd_depth_25bps": levels[25],
        "usd_depth_50bps": levels[50],
    }