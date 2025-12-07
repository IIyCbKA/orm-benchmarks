import asyncio
import time
from datetime import datetime, timedelta, UTC
from decimal import Decimal

from sqlalchemy import select, func
from tests_async.db import AsyncSessionLocal
from models import Booking


async def main() -> None:
    now = datetime.now(UTC)
    date_from = now - timedelta(days=30)
    amount_low = Decimal('50.00')
    amount_high = Decimal('500.00')

    start = time.time()

    try:
        async with AsyncSessionLocal() as session:
            statement = (
                select(func.count())
                .select_from(Booking)
                .where(
                    Booking.total_amount.between(amount_low, amount_high),
                    Booking.book_date >= date_from,
                )
            )

            await session.execute(statement)
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy Async. Test 4. Filter large\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    asyncio.run(main())
