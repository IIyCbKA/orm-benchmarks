from datetime import datetime, timedelta, UTC
from decimal import Decimal
from tests_sync.db import SessionLocal
from sqlalchemy import select, func
from models import Booking
import time


def main() -> None:
    now = datetime.now(UTC)
    date_from = now - timedelta(days=30)
    amount_low = Decimal('50.00')
    amount_high = Decimal('500.00')
    start = time.time()

    with SessionLocal() as session:
        try:
            statement = (
                select(func.count())
                .select_from(Booking)
                .where(
                    Booking.total_amount.between(amount_low, amount_high),
                    Booking.book_date >= date_from,
                )
            )
            session.execute(statement)
        except Exception:
            pass

    end = time.time()
    elapsed = end - start

    print(
        f'SQLAlchemy. Test 4. Filter large\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    main()
