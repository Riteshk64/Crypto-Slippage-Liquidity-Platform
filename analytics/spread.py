from typing import Any


def calculate_spread(
    binance_orderbook: dict[str, Any],
    kraken_orderbook: dict[str, Any],
) -> dict[str, float]:

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

    return {
        "binance_bid": binance_bid,
        "binance_ask": binance_ask,
        "kraken_bid": kraken_bid,
        "kraken_ask": kraken_ask,
        "spread_bps": spread_bps,
    }