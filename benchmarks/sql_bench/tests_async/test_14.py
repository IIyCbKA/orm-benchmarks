import asyncio
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
                    DELETE FROM bookings.tickets
                    USING bookings.bookings b
                    WHERE tickets.book_ref = b.id AND b.book_ref = $1
                    """,
                    generate_book_ref(i)
                )

                await conn.execute(
                    """
                    DELETE FROM bookings.bookings
                    WHERE book_ref = $1
                    """,
                    generate_book_ref(i)
                )
            finally:
                await conn.close()
    except Exception:
        pass

    elapsed = time.time() - start
    print(
        f'Pure async SQL (asyncpg). Test 14. Batch delete. {COUNT} entries\n'
        f'elapsed_sec={elapsed:.4f};'
    )

if __name__ == "__main__":
    asyncio.run(main())
