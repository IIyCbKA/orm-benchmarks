import asyncio
from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time
from tests_async.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))

def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'

def get_new_amount(i: int) -> Decimal:
    return Decimal(i + 100) / Decimal("10.00")

@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)

async def main() -> None:
    start = time.time()

    try:
        for i in range(COUNT):
            conn = await get_connection()
            try:
                await conn.execute(
                    """
                    UPDATE bookings.bookings
                    SET total_amount = $1,
                        book_date = $2
                    WHERE book_ref = $3
                    """,
                    get_new_amount(i),
                    get_curr_date(),
                    generate_book_ref(i)
                )
            finally:
                await conn.close()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'Pure async SQL (asyncpg). Test 12. Single update. {COUNT} entries\n'
        f'elapsed_sec={elapsed:.4f};'
    )

if __name__ == "__main__":
    asyncio.run(main())
