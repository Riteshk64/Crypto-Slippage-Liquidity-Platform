from analytics.spread import calculate_spread
from analytics.arb_state import signal_state


def get_arb_signal(
    binance_orderbook,
    kraken_orderbook,
    threshold_bps: float = 10.0,
) -> dict:

    spread = calculate_spread(
        binance_orderbook,
        kraken_orderbook,
    )

    buy_binance = spread[
        "buy_binance_sell_kraken_bps"
    ]

    buy_kraken = spread[
        "buy_kraken_sell_binance_bps"
    ]

    best_spread = max(
        buy_binance,
        buy_kraken,
    )

    current_signal = None
    current_spread = 0.0

    if buy_binance > threshold_bps:
        current_signal = (
            "buy_binance_sell_kraken"
        )
        current_spread = buy_binance

    elif buy_kraken > threshold_bps:
        current_signal = (
            "buy_kraken_sell_binance"
        )
        current_spread = buy_kraken

    if current_signal == signal_state["signal"]:
        signal_state["count"] += 1

    else:
        signal_state["signal"] = current_signal
        signal_state["count"] = (
            1 if current_signal else 0
        )

    return {
        "signal": current_signal or "none",
        "spread_bps": current_spread,
        "current_best_spread_bps": best_spread,
        "threshold_bps": threshold_bps,
        "consecutive_observations": signal_state["count"],
        "confirmed": signal_state["count"] >= 5,
    }