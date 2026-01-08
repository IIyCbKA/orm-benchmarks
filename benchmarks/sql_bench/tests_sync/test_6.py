import time
import sys
from tests_sync.db import get_connection

def main() -> None:
    start = time.perf_counter_ns()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM bookings.bookings ORDER BY book_ref LIMIT 1")
                _ = cur.fetchone()
    except Exception as e:
        print(f'[ERROR] Test 6 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure SQL (psycopg3). Test 6. Find first\n'
        f'elapsed_ns={elapsed}'
    )

if __name__ == "__main__":
    main()
