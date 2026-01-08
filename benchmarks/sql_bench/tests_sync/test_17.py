import os
import time
import sys
from tests_sync.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'd{i:05d}'


def main() -> None:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    start = time.perf_counter_ns()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                for book_ref in refs:
                    cur.execute(
                        "DELETE FROM bookings.tickets WHERE book_ref = %s",
                        (book_ref,)
                    )
                    cur.execute(
                        "DELETE FROM bookings.bookings WHERE book_ref = %s",
                        (book_ref,)
                    )
                    conn.commit()
    except Exception as e:
        print(f"[ERROR] Test 17 failed: {e}")
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start
    print(
        f'Pure SQL (psycopg3). Test 17. Nested delete. {COUNT} entries\n'
        f'elapsed_ns={elapsed}'
    )


if __name__ == "__main__":
    main()
