from datetime import datetime, UTC
from decimal import Decimal
from tests_async.db import AsyncSessionLocal
from models import Booking
import os
import time
import asyncio

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def generate_amount(i: int) -> Decimal:
    value = i + 500
    return Decimal(value) / Decimal('10.00')


async def main() -> None:
    start = time.time()

    for i in range(COUNT):
        async with AsyncSessionLocal() as session:
            try:
                item = Booking(
                    book_ref=generate_book_ref(i),
                    book_date=datetime.now(UTC),
                    total_amount=generate_amount(i),
                )
                session.add(item)
                await session.commit()
            except Exception:
                pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy Async. Test 1. Insert\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    asyncio.run(main())
