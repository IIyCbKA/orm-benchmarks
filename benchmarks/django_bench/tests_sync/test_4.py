from decimal import Decimal
from functools import lru_cache
import os
import statistics
import sys
import time

import django
django.setup()

from core.models import Booking, Ticket
from django.db import transaction
from django.utils import timezone

ITERATION_COUNT = int(os.environ.get('ITERATIONS', '2500'))
NESTED_COUNT = int(os.environ.get('NESTED_COUNT', '5'))


def generate_book_ref(i: int) -> str:
  return f'd{i:05d}'


def generate_ticket_no(i: int, j: int) -> str:
  return f'98{j:04d}{i:07d}'


def generate_passenger_id(i: int, j: int) -> str:
  return f'p{j:04d}{i:04d}'


def generate_amount(i: int) -> Decimal:
  value = i + 500
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return timezone.now()


def create_iteration(i: int) -> int:
  start = time.perf_counter_ns()

  with transaction.atomic():
    booking = Booking.objects.create(
      book_ref=generate_book_ref(i),
      book_date=get_curr_date(),
      total_amount=generate_amount(i),
    )

    for j in range(NESTED_COUNT):
      _ = Ticket.objects.create(
        ticket_no=generate_ticket_no(i, j),
        book_ref=booking,
        passenger_id=generate_passenger_id(i, j),
        passenger_name='Test',
        outbound=True
      )

  end = time.perf_counter_ns()
  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for i in range(ITERATION_COUNT):
      results.append(create_iteration(i))
  except Exception as e:
    print(f'[ERROR] Test 4 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'Django ORM (sync). Test 4. Nested create\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
