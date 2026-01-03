import asyncio
import sys
import time

import django
django.setup()

from core.models import Booking

async def main() -> None:
  start = time.perf_counter_ns()

  try:
    _ = [b async for b in Booking.objects.all()]
  except Exception as e:
    print(f'[ERROR] Test 5 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 5. Find all\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())
