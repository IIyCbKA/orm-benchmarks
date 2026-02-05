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
from django.utils import timezone
from django.db import transaction

from django.db import connection
connection.ensure_connection()

COUNT = int(os.environ.get('ITERATIONS', '2500'))
BATCH_SIZE = int(os.environ.get('BATCH_SIZE', '50'))
BATCH_COUNT = COUNT // BATCH_SIZE


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


@lru_cache(1)
def get_curr_date():
  return timezone.now()


@sync_to_async
def update_booking_sync(bookings: list[Booking]) -> None:
  with transaction.atomic():
    for booking in bookings:
      booking.total_amount /= Decimal('10.00')
      booking.book_date = get_curr_date()
      booking.save(update_fields=['total_amount', 'book_date'])


async def main() -> None:
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    bookings = [b async for b in Booking.objects.filter(book_ref__in=refs)]

    coroutines = [
      update_booking_sync(bookings[i * BATCH_SIZE:(i + 1) * BATCH_SIZE])
      for i in range(BATCH_COUNT)
    ]

    start = time.perf_counter_ns()

    await asyncio.gather(*coroutines)

    end = time.perf_counter_ns()
  except Exception as e:
    print(f'[ERROR] Test 11 failed: {e}')
    sys.exit(1)

  elapsed = end - start

  print(
    f'Django ORM (async). Test 11. Transaction update. '
    f'{BATCH_COUNT} transaction, {BATCH_SIZE} updates per transaction\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())
