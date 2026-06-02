import asyncio
import json
from typing import Any
import logging
import websockets

from storage.state import kraken_orderbook

logger = logging.getLogger(__name__)

def apply_updates(side: list[list[str]],updates: list[dict[str, Any]],reverse: bool,) -> list[list[str]]:
    levels: dict[str, str] = {
        price: qty
        for price, qty in side
    }

    for level in updates:
        price: str = str(level["price"])
        qty: str = str(level["qty"])

        if float(qty) == 0:
            levels.pop(price, None)
        else:
            levels[price] = qty

    updated_side: list[list[str]] = [
        [price, qty]
        for price, qty in levels.items()
    ]

    updated_side.sort(
        key=lambda level: float(level[0]),
        reverse=reverse,
    )

    return updated_side[:10]


async def stream() -> None:
    url: str = "wss://ws.kraken.com/v2"

    while True:
        try:
            async with websockets.connect(
                url,
                ping_interval=20,
                ping_timeout=20,
            ) as ws:
                await ws.send(
                    json.dumps(
                        {
                            "method": "subscribe",
                            "params": {
                                "channel": "book",
                                "symbol": ["BTC/USD"],
                                "depth": 10,
                            },
                        }
                    )
                )

                while True:
                    msg: str = await ws.recv()
                    data: dict[str, Any] = json.loads(msg)

                    if data.get("channel") != "book":
                        continue

                    book: dict[str, Any] = data["data"][0]

                    if data["type"] == "snapshot":
                        kraken_orderbook["bids"] = [
                            [str(level["price"]), str(level["qty"])]
                            for level in book["bids"]
                        ]

                        kraken_orderbook["asks"] = [
                            [str(level["price"]), str(level["qty"])]
                            for level in book["asks"]
                        ]

                        continue

                    if book["bids"]:
                        kraken_orderbook["bids"] = apply_updates(
                            side=kraken_orderbook["bids"],
                            updates=book["bids"],
                            reverse=True,
                        )

                    if book["asks"]:
                        kraken_orderbook["asks"] = apply_updates(
                            side=kraken_orderbook["asks"],
                            updates=book["asks"],
                            reverse=False,
                        )

        except Exception as exc:
            logger.warning("Kraken websocket error: %s",exc)

        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(stream())