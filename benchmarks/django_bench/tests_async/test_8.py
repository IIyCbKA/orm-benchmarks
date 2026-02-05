from decimal import Decimal
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

LIMIT = int(os.environ.get('LIMIT', '250'))
OFFSET = int(os.environ.get('OFFSET', '500'))
SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))

AMOUNT_LOW = Decimal('50.00')
AMOUNT_HIGH = Decimal('500.00')


async def select_iteration() -> None:
  _ = [r async for r in Booking.objects.filter(
    total_amount__gte=AMOUNT_LOW,
    total_amount__lte=AMOUNT_HIGH
  ).order_by('total_amount')[OFFSET:OFFSET + LIMIT]]


async def main() -> None:
  try:
    coroutines = [select_iteration() for _ in range(SELECT_REPEATS)]

    start = time.perf_counter_ns()

    await asyncio.gather(*coroutines)

    end = time.perf_counter_ns()
  except Exception as e:
    print(f'[ERROR] Test 8 failed: {e}')
    sys.exit(1)

  elapsed = end - start

  print(
    f'Django ORM (async). Test 8. Find with filter, offset pagination and sort.\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())
