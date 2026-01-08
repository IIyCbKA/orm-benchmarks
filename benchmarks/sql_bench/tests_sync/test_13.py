from decimal import Decimal
import os
import time
import sys
from tests_sync.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def main() -> None:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    start = time.perf_counter_ns()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                for ref in refs:
                    cur.execute(
                        """
                        UPDATE bookings.bookings
                        SET total_amount = total_amount + %s
                        WHERE book_ref = %s
                        """,
                        (Decimal('10.00'), ref)
                    )
                    cur.execute(
                        """
                        UPDATE bookings.tickets t
                        SET passenger_name = %s
                        FROM bookings.bookings b
                        WHERE t.book_ref = b.book_ref AND b.book_ref = %s
                        """,
                        ('Nested update', ref)
                    )
                    conn.commit()
    except Exception as e:
        print(f'[ERROR] Test 13 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure SQL (psycopg3). Test 13. Nested update. {COUNT} entries\n'
        f'elapsed_ns={elapsed}'
    )

if __name__ == "__main__":
    main()
