from decimal import Decimal
from datetime import datetime, UTC
import os
import time
from tests_sync.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))

def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'

def main() -> None:
    start = time.time()

    try:
        for i in range(COUNT):
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE bookings.bookings
                        SET total_amount = total_amount + %s
                        WHERE book_ref = %s
                        """,
                        (Decimal('10.00'), generate_book_ref(i))
                    )
                    cur.execute(
                        """
                        UPDATE bookings.tickets t
                        SET passenger_name = %s
                        FROM bookings.bookings b
                        WHERE t.book_ref = b.id AND b.book_ref = %s
                        """,
                        ('Nested update', generate_book_ref(i))
                    )
                conn.commit()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'Pure SQL (psycopg3). Test 13. Nested batch update. {COUNT} entries\n'
        f'elapsed_sec={elapsed:.4f};'
    )

if __name__ == "__main__":
    main()
