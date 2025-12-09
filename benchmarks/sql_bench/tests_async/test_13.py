import asyncio
from decimal import Decimal
from datetime import datetime, UTC
import os
import time
from tests_async.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))

def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'

async def main() -> None:
    start = time.time()

    try:
        for i in range(COUNT):
            conn = await get_connection()
            try:
                await conn.execute(
                    """
                    UPDATE bookings.bookings
                    SET total_amount = total_amount + $1
                    WHERE book_ref = $2
                    """,
                    Decimal('10.00'),
                    generate_book_ref(i)
                )

                await conn.execute(
                    """
                    UPDATE bookings.tickets t
                    SET passenger_name = $1
                    FROM bookings.bookings b
                    WHERE t.book_ref = b.id AND b.book_ref = $2
                    """,
                    'Nested update',
                    generate_book_ref(i)
                )
            finally:
                await conn.close()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'Pure async SQL (asyncpg). Test 13. Nested batch update. {COUNT} entries\n'
        f'elapsed_sec={elapsed:.4f};'
    )

if __name__ == "__main__":
    asyncio.run(main())
