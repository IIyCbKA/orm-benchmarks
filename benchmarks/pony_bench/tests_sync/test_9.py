from pony.orm import db_session, select
from core.models import Ticket
import time

def generate_book_ref(i: int) -> str:
  return f'd{i:05d}'


def main() -> None:
  start = time.perf_counter_ns()

  with db_session():
    try:
      _ = list(
        select((t, t.book_ref)
        for t in Ticket
        if t.book_ref.book_ref == generate_book_ref(1))
      )
    except Exception:
      pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 9. Nested find unique\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  main()