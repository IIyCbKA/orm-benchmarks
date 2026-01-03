import sys
import time

import django
django.setup()

from core.models import Booking

def main() -> None:
  start = time.perf_counter_ns()

  try:
    _ = Booking.objects.first()
  except Exception as e:
    print(f'[ERROR] Test 6 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 6. Find first\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
