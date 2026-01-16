from pony.orm import db_session, commit, select
from core.models import Booking
import os
import statistics
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'b{i:05d}'


@db_session
def main() -> None:
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    bookings = list(select(b for b in Booking if b.book_ref in refs))
  except Exception as e:
    print(f'[ERROR] Test 15 failed (data preparation): {e}')
    sys.exit(1)

  results: list[int] = []

  try:
    for booking in bookings:
      start = time.perf_counter_ns()

      booking.delete()
      commit()

      end = time.perf_counter_ns()
      results.append(end - start)
  except Exception as e:
    print(f'[ERROR] Test 15 failed (delete phase): {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'PonyORM. Test 15. Single delete\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()