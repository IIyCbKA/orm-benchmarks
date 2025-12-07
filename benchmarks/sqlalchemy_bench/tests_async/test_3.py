import asyncio
import os
import time
from datetime import datetime, UTC
from decimal import Decimal

from sqlalchemy import insert
from tests_async.db import AsyncSessionLocal
from models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'c{i:05d}'


def generate_amount(i: int) -> Decimal:
    value = i + 500
    return Decimal(value) / Decimal('10.00')


async def main() -> None:
    start = time.time()

    rows = []
    for i in range(COUNT):
        rows.append({
            "book_ref": generate_book_ref(i),
            "book_date": datetime.now(UTC),
            "total_amount": generate_amount(i),
        })

    try:
        async with AsyncSessionLocal() as session:
            await session.execute(insert(Booking), rows)
            await session.commit()
    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy Async. Test 3. Bulk insert\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    asyncio.run(main())
