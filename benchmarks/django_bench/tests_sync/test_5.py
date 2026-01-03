import sys
import time

import django
django.setup()

from core.models import Booking

def main() -> None:
  start = time.perf_counter_ns()

  try:
    _ = list(Booking.objects.all())
  except Exception as e:
    print(f'[ERROR] Test 5 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 5. Find all\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
