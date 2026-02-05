import asyncio
import os
import sys
import time

import django
django.setup()

from core.models import Booking

from django.db import connection
connection.ensure_connection()

SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


async def select_iteration() -> None:
  _ = await Booking.objects.afirst()


async def main() -> None:
  try:
    coroutines = [select_iteration() for _ in range(SELECT_REPEATS)]

    start = time.perf_counter_ns()

    await asyncio.gather(*coroutines)

    end = time.perf_counter_ns()
  except Exception as e:
    print(f'[ERROR] Test 5 failed: {e}')
    sys.exit(1)

  elapsed = end - start

  print(
    f'Django ORM (async). Test 5. Find first. {SELECT_REPEATS} queries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())
