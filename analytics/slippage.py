from typing import Any

def estimate_buy_slippage(orderbook: dict[str, Any], usd_size: float) -> dict[str, float]:
    remaining: float = usd_size
    btc_bought: float = 0.0

    for price, qty in orderbook["asks"]:
        ask_price: float = float(price)
        ask_qty: float = float(qty)

        level_value: float = ask_price * ask_qty

        if remaining >= level_value:
            btc_bought += ask_qty
            remaining -= level_value
        else:
            btc_bought += remaining / ask_price
            remaining = 0.0
            break

    if btc_bought == 0:
        raise ValueError("No ask liquidity available")

    filled_usd: float = usd_size - remaining
    avg_price: float = filled_usd / btc_bought

    best_ask: float = float(orderbook["asks"][0][0])

    slippage_bps: float = ((avg_price - best_ask) / best_ask) * 10000

    return {
        "best_ask": best_ask,
        "avg_price": avg_price,
        "filled_usd": filled_usd,
        "unfilled_usd": remaining,
        "slippage_bps": slippage_bps,
    }