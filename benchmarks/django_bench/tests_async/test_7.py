import asyncio
import sys
import time

import django
django.setup()

from core.models import Ticket

async def main() -> None:
  start = time.perf_counter_ns()

  try:
    _ = await Ticket.objects.select_related('book_ref').afirst()
  except Exception as e:
    print(f'[ERROR] Test 7 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 7. Nested find first\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())
