from datetime import datetime, UTC
from decimal import Decimal
from pony.orm import db_session, commit
from random import randint
from models import Booking
import os
import secrets
import string
import time

ALPHANUM = string.digits + string.ascii_lowercase + string.ascii_uppercase
COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref() -> str:
  return ''.join(secrets.choice(ALPHANUM) for _ in range(6))


def generate_amount() -> Decimal:
  cents = randint(1000, 99999)
  return Decimal(cents) / Decimal('100.00')


def main() -> None:
  start = time.time()

  with db_session():
    for _ in range(COUNT):
      try:
        Booking(
          book_ref=generate_book_ref(),
          book_date=datetime.now(UTC),
          total_amount=generate_amount(),
        )

      except Exception:
        pass

    commit()

  end = time.time()
  elapsed = end - start

  rows_per_sec = COUNT / elapsed
  rows_per_min = rows_per_sec * 60.0

  print(
    f'PonyORM. Test 2.\n'
    f'rows={COUNT}; elapsed_sec={elapsed:.4f};'
    f'rpm={rows_per_min:.2f}; rps={rows_per_sec:.2f}'
  )


if __name__ == '__main__':
  main()
