from decimal import Decimal
from functools import lru_cache
import asyncio
import os
import sys
import time

import django
django.setup()

from core.models import Booking
from django.utils import timezone

from django.db import connection
connection.ensure_connection()

COUNT = int(os.environ.get('ITERATIONS', '2500'))
BATCH_SIZE = int(os.environ.get('BATCH_SIZE', '50'))
BATCH_COUNT = COUNT // BATCH_SIZE


def generate_book_ref(i: int) -> str:
  return f'c{i:05d}'


def generate_amount(i: int) -> Decimal:
  value = i + 500
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return timezone.now()


async def bulk_create(batch_offset: int) -> None:
  objs = [
    Booking(
      book_ref=generate_book_ref(batch_offset + i),
      book_date=get_curr_date(),
      total_amount=generate_amount(batch_offset + i),
    ) for i in range(BATCH_SIZE)
  ]

  await Booking.objects.abulk_create(objs)


async def main() -> None:
  try:
    coroutines = [bulk_create(i * BATCH_COUNT) for i in range(COUNT)]

    start = time.perf_counter_ns()

    await asyncio.gather(*coroutines)

    end = time.perf_counter_ns()
  except Exception as e:
    print(f'[ERROR] Test 3 failed: {e}')
    sys.exit(1)

  elapsed = end - start

  print(
    f'Django ORM (async). Test 3. Bulk create. '
    f'{BATCH_COUNT} bulk-inserts, {BATCH_SIZE} inserts per bulk\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())
