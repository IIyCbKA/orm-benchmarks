import asyncio
import os
import sys
import time

import django
django.setup()

from core.models import Ticket

from django.db import connection
connection.ensure_connection()

LIMIT = int(os.environ.get('LIMIT', '250'))
SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


async def select_iteration() -> None:
  _ = [row async for row in
    Ticket.objects.values_list(
      'ticket_no',
      'book_ref',
      'passenger_id',
      'passenger_name',
      'outbound',
      'book_ref__book_ref',
      'book_ref__book_date',
      'book_ref__total_amount',
    ).order_by('ticket_no')[:LIMIT]
  ]


async def main() -> None:
  try:
    coroutines = [select_iteration() for _ in range(SELECT_REPEATS)]

    start = time.perf_counter_ns()

    await asyncio.gather(*coroutines)

    end = time.perf_counter_ns()
  except Exception as e:
    print(f'[ERROR] Test 7 failed: {e}')
    sys.exit(1)

  elapsed = end - start

  print(
    f'Django ORM (async). Test 7. Find with limit and include parent. {SELECT_REPEATS} queries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())
