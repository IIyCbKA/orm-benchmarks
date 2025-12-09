import time
from tests_sync.db import get_connection


def main() -> None:
    start = time.time()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM bookings.bookings ORDER BY book_ref LIMIT 1")
                first_booking = cur.fetchone()

                ticket_count = 0
                if first_booking:
                    booking_id = first_booking[0]
                    cur.execute("SELECT COUNT(*) FROM bookings.tickets WHERE book_ref_id = %s", (booking_id,))
                    ticket_count = cur.fetchone()[0]
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'Pure SQL (psycopg3). Test 7. Nested find first\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == "__main__":
    main()
