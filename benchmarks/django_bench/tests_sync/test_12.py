from decimal import Decimal
from functools import lru_cache
import os
import statistics
import sys
import time

import django
django.setup()

from core.models import Booking
from django.utils import timezone

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


@lru_cache(1)
def get_curr_date():
  return timezone.now()


def main() -> None:
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    bookings = list(Booking.objects.filter(book_ref__in=refs))
  except Exception as e:
    print(f'[ERROR] Test 12 failed (data preparation): {e}')
    sys.exit(1)

  results: list[int] = []

  try:
    for booking in bookings:
      start = time.perf_counter_ns()

      booking.total_amount /= Decimal('10.00')
      booking.book_date = get_curr_date()
      booking.save(update_fields=['total_amount', 'book_date'])

      end = time.perf_counter_ns()
      results.append(end - start)
  except Exception as e:
    print(f'[ERROR] Test 12 failed (update phase): {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'Django ORM (sync). Test 12. Single update\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()