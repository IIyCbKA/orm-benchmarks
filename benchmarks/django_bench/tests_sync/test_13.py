from decimal import Decimal
import os
import statistics
import sys
import time

import django
django.setup()

from core.models import Booking, Ticket
from django.db import transaction

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'd{i:05d}'


def main() -> None:
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    bookings = list(Booking.objects.filter(book_ref__in=refs))
  except Exception as e:
    print(f'[ERROR] Test 13 failed (data preparation): {e}')
    sys.exit(1)

  results: list[int] = []

  try:
    for booking in bookings:
      start = time.perf_counter_ns()

      with transaction.atomic():
        booking.total_amount += Decimal('10.00')
        booking.save(update_fields=['total_amount'])
        Ticket.objects.filter(
          book_ref=booking.book_ref).update(passenger_name='Nested update')

      end = time.perf_counter_ns()
      results.append(end - start)
  except Exception as e:
    print(f'[ERROR] Test 13 failed (update phase): {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'Django ORM (sync). Test 13. Nested update\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()