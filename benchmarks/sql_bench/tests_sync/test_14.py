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
                        DELETE FROM bookings.tickets
                        USING bookings.bookings b
                        WHERE tickets.book_ref = b.id AND b.book_ref = %s
                        """,
                        (generate_book_ref(i),)
                    )
                    cur.execute(
                        """
                        DELETE FROM bookings.bookings
                        WHERE book_ref = %s
                        """,
                        (generate_book_ref(i),)
                    )
                conn.commit()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'Pure SQL (psycopg3). Test 14. Batch delete. {COUNT} entries\n'
        f'elapsed_sec={elapsed:.4f};'
    )

if __name__ == "__main__":
    main()
