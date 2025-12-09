import asyncio
import time
from tests_async.db import get_connection

async def main() -> None:
    start = time.time()
    ticket_count = 0

    try:
        conn = await get_connection()
        try:
            first_booking = await conn.fetchrow(
                "SELECT id FROM bookings.bookings ORDER BY book_ref LIMIT 1"
            )

            if first_booking:
                booking_id = first_booking['id']
                ticket_result = await conn.fetchrow(
                    "SELECT COUNT(*) AS cnt FROM bookings.tickets WHERE book_ref_id = $1",
                    booking_id
                )
                ticket_count = ticket_result['cnt'] if ticket_result else 0
        finally:
            await conn.close()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'Pure async SQL (asyncpg). Test 7. Nested find first\n'
        f'elapsed_sec={elapsed:.4f};'
    )

if __name__ == "__main__":
    asyncio.run(main())
