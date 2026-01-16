from pony.orm import db_session, select, commit
from core.models import Booking
import os
import sys

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'c{i:05d}'


@db_session
def main() -> None:
  """
  Pony ORM does not support true bulk delete as of 16.01.2026.
  Therefore, Test 16 "Bulk delete" is skipped for Pony,
  and we mark it with a dash in benchmarks.

  To maintain dataset consistency with other ORMs and clean the table for subsequent tests,
  this script deletes the required Booking entities one by one.
  """

  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    bookings = list(select(b for b in Booking if b.book_ref in refs))
  except Exception as e:
    print(f'[ERROR] Dataset preparation failed (instead of bulk delete): {e}')
    sys.exit(1)

  try:
    for booking in bookings:
      booking.delete()
    commit()
  except Exception as e:
    print(f'[ERROR] Dataset delete failed (instead of bulk delete): {e}')
    sys.exit(1)

  print(
    f'PonyORM. Test 16. Bulk delete. {COUNT} entries\n'
    f'Bulk delete is not supported — deleted individually for dataset cleanup'
  )


if __name__ == '__main__':
  main()
