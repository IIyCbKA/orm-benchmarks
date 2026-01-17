from pony.orm import db_session, select, commit
from core.models import Booking
import os
import statistics
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'd{i:05d}'


@db_session
def main() -> None:
  """
  Pony heavily relies on the cache, so deleting nested objects is possible
  either with 1 + 1 queries to the DB (bypassing the cache) or with N + 1
  queries that perform a full iteration over the objects.

  This implementation uses the N + 1 approach, since working with an
  initialized parent object is considered mandatory.
  """
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    bookings = list(
      select(b for b in Booking if b.book_ref in refs)
      .prefetch(Booking.tickets)
    )
  except Exception as e:
    print(f'[ERROR] Test 17 failed (data preparation): {e}')
    sys.exit(1)

  results: list[int] = []

  try:
    for booking in bookings:
      start = time.perf_counter_ns()

      for ticket in booking.tickets:
        ticket.delete()
      booking.delete()
      commit()

      end = time.perf_counter_ns()
      results.append(end - start)
  except Exception as e:
    print(f'[ERROR] Test 17 failed (delete phase): {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'PonyORM. Test 17. Nested delete\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
