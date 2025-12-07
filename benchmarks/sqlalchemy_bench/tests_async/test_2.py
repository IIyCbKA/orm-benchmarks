import asyncio
import os
import time
from datetime import datetime, UTC
from decimal import Decimal

from tests_async.db import AsyncSessionLocal
from models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'b{i:05d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal('10.00')


async def main() -> None:
    start = time.time()

    try:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                for i in range(COUNT):
                    item = Booking(
                        book_ref=generate_book_ref(i),
                        book_date=datetime.now(UTC),
                        total_amount=generate_amount(i),
                    )
                    session.add(item)

    except Exception:
        pass

    elapsed = time.time() - start

    print(
        f'SQLAlchemy Async. Test 2. Transaction insert\n'
        f'elapsed_sec={elapsed:.4f};'
    )


if __name__ == '__main__':
    asyncio.run(main())
