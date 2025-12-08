from datetime import datetime, timedelta, UTC
from decimal import Decimal
import time

from tests_sync.db import get_connection


def main() -> None:
    now = datetime.now(UTC)
    date_from = now - timedelta(days=30)
    amount_low = Decimal("50.00")
    amount_high = Decimal("500.00")

    start = time.time()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM booking
                    WHERE total_amount BETWEEN %s AND %s
                      AND book_date >= %s
                    """,
                    (amount_low, amount_high, date_from),
                )
                cur.fetchone()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'Pure SQL (psycopg3). Test 4. Filter large\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    main()
