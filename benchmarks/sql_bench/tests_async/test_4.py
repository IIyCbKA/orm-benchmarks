import asyncio
import os
import time
from datetime import datetime, UTC
from decimal import Decimal

from tests_async.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'd{i:05d}'


def generate_ticket_no(i: int) -> str:
    return f'98{i:11d}'


def generate_passenger_id(i: int) -> str:
    return f'p{i:08d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal("10.00")


async def main() -> None:
    start = time.time()
    curr_date = datetime.now(UTC)

    try:
        conn = await get_connection()
        try:
            async with conn.transaction():
                for i in range(COUNT):
                    booking_id = await conn.fetchval(
                        """
                        INSERT INTO bookings.bookings (book_ref, book_date, total_amount)
                        VALUES ($1, $2, $3)
                        RETURNING id
                        """,
                        generate_book_ref(i),
                        curr_date,
                        generate_amount(i),
                    )

                    await conn.execute(
                        """
                        INSERT INTO bookings.tickets 
                        (ticket_no, book_ref_id, passenger_id, passenger_name, outbound)
                        VALUES ($1, $2, $3, $4, $5)
                        """,
                        generate_ticket_no(i),
                        booking_id,
                        generate_passenger_id(i),
                        "Test",
                        True,
                    )
        finally:
            await conn.close()
    except Exception:
        pass

    elapsed = time.time() - start
    print(
        f'Pure async SQL (asyncpg). Test 4. Nested create. {COUNT} entities\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == "__main__":
    asyncio.run(main())
