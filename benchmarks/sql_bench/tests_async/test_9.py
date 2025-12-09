import asyncio
import time
from tests_async.db import get_connection

def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'

async def main() -> None:
    start = time.time()
    tickets_count = 0

    try:
        conn = await get_connection()
        try:
            booking_row = await conn.fetchrow(
                "SELECT id FROM bookings.bookings WHERE book_ref = $1 LIMIT 1",
                generate_book_ref(1)
            )

            if booking_row:
                booking_id = booking_row['id']
                count_row = await conn.fetchrow(
                    "SELECT COUNT(*) AS cnt FROM bookings.tickets WHERE book_ref_id = $1",
                    booking_id
                )
                tickets_count = count_row['cnt'] if count_row else 0
        finally:
            await conn.close()
    except Exception:
        tickets_count = 0

    elapsed = time.time() - start

    print(
        f'Pure async SQL (asyncpg). Test 9. Nested find unique\n'
        f'elapsed_sec={elapsed:.4f};'
    )

if __name__ == "__main__":
    asyncio.run(main())
