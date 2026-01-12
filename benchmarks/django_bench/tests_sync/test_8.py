import os
import statistics
import sys
import time

import django
django.setup()

from core.models import Booking

SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def select_iteration() -> int:
  start = time.perf_counter_ns()

  _ = Booking.objects.get(pk=generate_book_ref(1))

  end = time.perf_counter_ns()
  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      results.append(select_iteration())
  except Exception as e:
    print(f'[ERROR] Test 8 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'Django ORM (sync). Test 8. Find unique\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
