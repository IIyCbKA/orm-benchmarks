from pony.orm import db_session
from core.models import Booking
import os
import statistics
import sys
import time

SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def select_iteration() -> int:
  start = time.perf_counter_ns()

  with db_session:
    _ = Booking.select().order_by(Booking.book_ref).first()

  end = time.perf_counter_ns()
  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      results.append(select_iteration())
  except Exception as e:
    print(f'[ERROR] Test 6 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'PonyORM. Test 6. Find first\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()