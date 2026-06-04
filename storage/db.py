import os

import asyncpg
from dotenv import load_dotenv

load_dotenv()

pool: asyncpg.Pool | None = None


async def connect_db() -> None:
    global pool

    pool = await asyncpg.create_pool(
        os.getenv("DATABASE_URL"),
        min_size=1,
        max_size=5,
    )


async def close_db() -> None:
    global pool

    if pool:
        await pool.close()


def get_pool():
    if pool is None:
        raise RuntimeError(
            "Database pool not initialized"
        )

    return pool