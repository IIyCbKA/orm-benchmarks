from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time
from tests_sync.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))

def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'

def get_new_amount(i: int) -> Decimal:
    return Decimal(i + 100) / Decimal("10.00")

@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)

def main() -> None:
    start = time.time()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                for i in range(COUNT):
                    cur.execute(
                        """
                        UPDATE bookings.bookings
                        SET total_amount = %s,
                            book_date = %s
                        WHERE book_ref = %s
                        """,
                        (get_new_amount(i), get_curr_date(), generate_book_ref(i))
                    )
            conn.commit()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'Pure SQL (psycopg3). Test 11. Batch update. {COUNT} entries\n'
        f'elapsed_sec={elapsed:.4f};'
    )

if __name__ == "__main__":
    main()
