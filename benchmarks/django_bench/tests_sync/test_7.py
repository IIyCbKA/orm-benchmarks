import sys
import time

import django
django.setup()

from core.models import Ticket

def main() -> None:
  start = time.perf_counter_ns()

  try:
    _ = Ticket.objects.select_related('book_ref').first()
  except Exception as e:
    print(f'[ERROR] Test 7 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 7. Nested find first\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
