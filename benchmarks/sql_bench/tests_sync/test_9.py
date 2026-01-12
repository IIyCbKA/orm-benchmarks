from tests_sync.db import conn
import os
import statistics
import sys
import time

SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def generate_book_ref(i: int) -> str:
    return f'd{i:05d}'


def select_iterations() -> int:
    start = time.perf_counter_ns()

    with conn.cursor() as cur:
        _ = cur.execute("""
            SELECT 
                tickets.ticket_no,
                tickets.book_ref,
                tickets.passenger_id,
                tickets.passenger_name,
                tickets.outbound,
                bookings.book_ref,
                bookings.book_date,
                bookings.total_amount
            FROM tickets
            INNER JOIN bookings ON (tickets.book_ref = bookings.book_ref)
            WHERE tickets.book_ref = %s
        """, (generate_book_ref(1),)).fetchall()

    end = time.perf_counter_ns()
    return end - start


def main() -> None:
    results: list[int] = []

    try:
        for _ in range(SELECT_REPEATS):
            results.append(select_iterations())
    except Exception as e:
        print(f'[ERROR] Test 9 failed: {e}')
        sys.exit(1)

    elapsed = statistics.median(results)

    print(
        f'Pure SQL (psycopg3). Test 9. Nested find\n'
        f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
    main()
