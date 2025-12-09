import asyncio
import time
from tests_async.db import get_connection

async def main() -> None:
    start = time.time()
    all_bookings = []

    try:
        conn = await get_connection()
        try:
            all_bookings = await conn.fetch("SELECT * FROM bookings.bookings")
        finally:
            await conn.close()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'Pure async SQL (asyncpg). Test 5. Find all\n'
        f'elapsed_sec={elapsed:.4f};'
    )

if __name__ == "__main__":
    asyncio.run(main())
