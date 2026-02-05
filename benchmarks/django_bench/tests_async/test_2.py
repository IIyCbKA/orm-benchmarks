from decimal import Decimal
from functools import lru_cache
import asyncio
import os
import sys
import time

import django
django.setup()

from asgiref.sync import sync_to_async
from core.models import Booking
from django.db import transaction
from django.utils import timezone

from django.db import connection
connection.ensure_connection()

COUNT = int(os.environ.get('ITERATIONS', '2500'))
BATCH_SIZE = int(os.environ.get('BATCH_SIZE', '50'))
BATCH_COUNT = COUNT // BATCH_SIZE


def generate_book_ref(i: int) -> str:
  return f'b{i:05d}'


def generate_amount(i: int) -> Decimal:
  value = i + 500
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return timezone.now()


@sync_to_async
def transaction_create_sync(batch_offset: int) -> None:
  with transaction.atomic():
    for i in range(BATCH_SIZE):
      Booking.objects.create(
        book_ref=generate_book_ref(batch_offset + i),
        book_date=get_curr_date(),
        total_amount=generate_amount(batch_offset + i),
      )


async def main() -> None:
  try:
    coroutines = [transaction_create_sync(i * BATCH_SIZE) for i in range(BATCH_COUNT)]

    start = time.perf_counter_ns()

    await asyncio.gather(*coroutines)

    end = time.perf_counter_ns()
  except Exception as e:
    print(f'[ERROR] Test 2 failed: {e}')
    sys.exit(1)

  elapsed = end - start

  print(
    f'Django ORM (async). Test 2. Transaction create. '
    f'{BATCH_COUNT} transaction, {BATCH_SIZE} inserts per transaction\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())
