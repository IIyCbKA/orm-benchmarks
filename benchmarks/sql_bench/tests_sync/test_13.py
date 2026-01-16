from decimal import Decimal
import os
import statistics
import sys
import time
from tests_sync.db import conn

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'd{i:05d}'


def main() -> None:
    try:
        refs = [generate_book_ref(i) for i in range(COUNT)]
        current_data = []
        with conn.cursor() as cur:
            for ref in refs:
                total_amount = cur.execute("""
                    SELECT total_amount
                    FROM bookings.bookings
                    WHERE book_ref = %s
                """, (ref,)).fetchone()[0]

                current_data.append((ref, total_amount))
    except Exception as e:
        print(f'[ERROR] Test 13 failed (data preparation): {e}')
        sys.exit(1)

    results: list[int] = []

    try:
        with conn.cursor() as cur:
            for ref, old_amount in current_data:
                start = time.perf_counter_ns()

                with conn.transaction():
                    cur.execute("""
                        UPDATE bookings.bookings
                        SET total_amount = %s
                        WHERE book_ref = %s
                    """, (old_amount + Decimal('10.00'), ref))

                    cur.execute("""
                        UPDATE bookings.tickets 
                        SET passenger_name = %s 
                        WHERE book_ref = %s
                    """, ('Nested update', ref))

                end = time.perf_counter_ns()
                results.append(end - start)
    except Exception as e:
        print(f'[ERROR] Test 13 failed (update phase): {e}')
        sys.exit(1)

    elapsed = statistics.median(results)

    print(
        f'Pure SQL (psycopg3). Test 13. Nested update\n'
        f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
    main()
