from datetime import datetime, timedelta, UTC
from decimal import Decimal
import os
import time
from tests_sync.db import get_connection

LIMIT = int(os.environ.get('LIMIT', '250'))
OFFSET = int(os.environ.get('OFFSET', '500'))

def main() -> None:
    now = datetime.now(UTC)
    date_from = now - timedelta(days=30)
    amount_low = Decimal('50.00')
    amount_high = Decimal('500.00')
    start = time.time()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM bookings.bookings
                    WHERE total_amount BETWEEN %s AND %s
                      AND book_date >= %s
                    ORDER BY total_amount ASC
                    LIMIT %s OFFSET %s
                    """,
                    (amount_low, amount_high, date_from, LIMIT, OFFSET)
                )
                rows = cur.fetchall()
    except Exception:
        rows = []

    elapsed = time.time() - start

    print(
        f'Pure SQL (psycopg3). Test 10. Filter, paginate & sort\n'
        f'rows_fetched={len(rows)}; '
        f'elapsed_sec={elapsed:.4f};'
    )

if __name__ == "__main__":
    main()
