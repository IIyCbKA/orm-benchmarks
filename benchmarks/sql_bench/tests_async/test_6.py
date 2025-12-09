import asyncio
import time
from tests_async.db import get_connection

async def main() -> None:
    start = time.time()
    first_booking = None

    try:
        conn = await get_connection()
        try:
            first_booking = await conn.fetchrow(
                "SELECT * FROM bookings.bookings ORDER BY book_ref LIMIT 1"
            )
        finally:
            await conn.close()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'Pure async SQL (asyncpg). Test 6. Find first\n'
        f'elapsed_sec={elapsed:.4f};'
    )

if __name__ == "__main__":
    asyncio.run(main())
