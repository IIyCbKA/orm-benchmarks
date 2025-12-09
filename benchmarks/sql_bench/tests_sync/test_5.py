import time
from tests_sync.db import get_connection

def main() -> None:
    start = time.time()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM bookings.bookings")
                all_bookings = cur.fetchall()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'Pure SQL (psycopg3). Test 5. Find all\n'
        f'elapsed_sec={elapsed:.4f};'
    )

if __name__ == "__main__":
    main()
