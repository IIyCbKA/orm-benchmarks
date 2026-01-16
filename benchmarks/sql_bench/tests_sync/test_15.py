import os
import statistics
import sys
import time
from tests_sync.db import conn

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'b{i:05d}'


def main() -> None:
    refs = [generate_book_ref(i) for i in range(COUNT)]

    results: list[int] = []

    try:
        for ref in refs:
            start = time.perf_counter_ns()

            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM bookings.bookings
                    WHERE book_ref IN (%s)
                """, (ref,))

            end = time.perf_counter_ns()
            results.append(end - start)
    except Exception as e:
        print(f'[ERROR] Test 15 failed: {e}')
        sys.exit(1)

    elapsed = statistics.median(results)

    print(
        f'Pure SQL (psycopg3). Test 15. Single delete\n'
        f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
    main()
