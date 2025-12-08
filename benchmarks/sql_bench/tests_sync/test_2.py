from datetime import datetime, UTC
from decimal import Decimal
import os
import time

from tests_sync.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'b{i:05d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal("10.00")


def main() -> None:
    start = time.time()


    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                for i in range(COUNT):
                    cur.execute(
                        """
                        INSERT INTO booking (book_ref, book_date, total_amount)
                        VALUES (%s, %s, %s)
                        """,
                        (
                            generate_book_ref(i),
                            datetime.now(UTC),
                            generate_amount(i),
                        ),
                    )
            conn.commit()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'Pure SQL (psycopg3). Test 2. Transaction insert\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == "__main__":
    main()
