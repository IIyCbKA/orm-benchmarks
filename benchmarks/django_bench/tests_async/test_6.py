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


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


async def select_iteration() -> None:
  _ = await Booking.objects.aget(pk=generate_book_ref(1))


async def main() -> None:
  try:
    coroutines = [select_iteration() for _ in range(SELECT_REPEATS)]

    start = time.perf_counter_ns()

    await asyncio.gather(*coroutines)

    end = time.perf_counter_ns()
  except Exception as e:
    print(f'[ERROR] Test 6 failed: {e}')
    sys.exit(1)

  elapsed = end - start

  print(
    f'Django ORM (async). Test 6. Find unique record. {SELECT_REPEATS} queries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())
