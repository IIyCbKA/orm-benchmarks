import time
from tests_sync.db import get_connection


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def main() -> None:
    start = time.time()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM bookings.bookings WHERE book_ref = %s LIMIT 1",
                    (generate_book_ref(1),)
                )
                booking_row = cur.fetchone()

                tickets_count = 0
                if booking_row:
                    booking_id = booking_row[0]
                    cur.execute(
                        "SELECT COUNT(*) FROM bookings.tickets WHERE book_ref_id = %s",
                        (booking_id,)
                    )
                    tickets_count = cur.fetchone()[0]

    except Exception:
        tickets_count = 0

    elapsed = time.time() - start

    print(
        f'Pure SQL (psycopg3). Test 9. Nested find unique\n'
        f'tickets_count={tickets_count}; '
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == "__main__":
    main()
