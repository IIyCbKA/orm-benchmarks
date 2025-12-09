from datetime import datetime, UTC
from decimal import Decimal
import os
import time

from tests_sync.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'd{i:05d}'


def generate_ticket_no(i: int) -> str:
    return f'98{i:11d}'


def generate_passenger_id(i: int) -> str:
    return f'p{i:08d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal("10.00")


def main() -> None:
    start = time.time()
    curr_date = datetime.now(UTC)

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                for i in range(COUNT):
                    # Вставка booking
                    cur.execute(
                        """
                        INSERT INTO bookings.bookings (book_ref, book_date, total_amount)
                        VALUES (%s, %s, %s)
                        RETURNING id
                        """,
                        (generate_book_ref(i), curr_date, generate_amount(i))
                    )
                    booking_id = cur.fetchone()[0]

                    cur.execute(
                        """
                        INSERT INTO bookings.tickets 
                        (ticket_no, book_ref_id, passenger_id, passenger_name, outbound)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            generate_ticket_no(i),
                            booking_id,
                            generate_passenger_id(i),
                            "Test",
                            True,
                        )
                    )
                conn.commit()
    except Exception:
        pass

    elapsed = time.time() - start
    print(
        f'Pure SQL (psycopg3). Test 4. Nested create. {COUNT} entities\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == "__main__":
    main()
