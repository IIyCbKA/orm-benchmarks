from pony.orm import db_session, select
from core.models import Ticket
import os
import statistics
import sys
import time

SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def generate_book_ref(i: int) -> str:
  return f'd{i:05d}'


def select_iteration() -> int:
  start = time.perf_counter_ns()

  with db_session:
    _ = list(
      select((
        t.ticket_no,
        t.book_ref,
        t.passenger_id,
        t.passenger_name,
        t.outbound,
        b.book_ref,
        b.book_date,
        b.total_amount
      ) for t in Ticket for b in t.book_ref if b.book_ref == generate_book_ref(1))
    )

  end = time.perf_counter_ns()
  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      results.append(select_iteration())
  except Exception as e:
    print(f'[ERROR] Test 9 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'PonyORM. Test 9. Nested find\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()