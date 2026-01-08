import time
import sys
from tests_sync.db import get_connection

def main() -> None:
    start = time.perf_counter_ns()
    connection = get_connection()
    try:
        with connection as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT bookings.book_ref, bookings.book_date, bookings.total_amount FROM bookings""")
                all_bookings = cur.fetchall()
    except Exception as e:
        print(f'[ERROR] Test 5 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure SQL (psycopg3). Test 5. Find all\n'
        f'elapsed_ns={elapsed};'
    )

if __name__ == "__main__":
    main()
