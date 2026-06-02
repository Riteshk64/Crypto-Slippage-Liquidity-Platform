import asyncio
import json
from typing import Any
import logging
import websockets

from storage.state import binance_orderbook

logger = logging.getLogger(__name__)

async def stream() -> None:
    url: str = (
        "wss://stream.binance.com:9443/ws/"
        "btcusdt@depth20@100ms"
    )

    while True:
        try:
            async with websockets.connect(
                url,
                ping_interval=20,
                ping_timeout=20,
            ) as ws:

                while True:
                    msg: str = await ws.recv()

                    data: dict[str, Any] = json.loads(
                        msg
                    )

                    binance_orderbook["bids"] = (
                        data["bids"]
                    )

                    binance_orderbook["asks"] = (
                        data["asks"]
                    )

        except Exception as exc:
            logger.warning("Binance websocket error: %s",exc)

        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(stream())