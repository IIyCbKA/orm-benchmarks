from decimal import Decimal
from pony.orm import db_session, select, commit, update
from core.models import Booking, Ticket
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
  Pony ORM does not support bulk update as of 16.01.2026.

  Because 1 question to db -> N questions to db on your server
  plus some additional RAM for nested objects
  """
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    bookings = list(
      select(b for b in Booking if b.book_ref in refs)
      .prefetch(Booking.tickets)
    )
  except Exception as e:
    print(f'[ERROR] Test 13 failed (data preparation): {e}')
    sys.exit(1)

  results: list[int] = []

  try:
    for booking in bookings:
      start = time.perf_counter_ns()

      booking.total_amount += Decimal('10.00')
      for ticket in booking.tickets:
        ticket.passenger_name = 'Nested update'
      commit()

      end = time.perf_counter_ns()
      results.append(end - start)
  except Exception as e:
    print(f'[ERROR] Test 13 failed (update phase): {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'PonyORM. Test 13. Nested update\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()