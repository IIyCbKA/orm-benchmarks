from pony.orm import db_session, select
from core.models import Ticket
import time

def main() -> None:
  start = time.perf_counter_ns()

  with db_session():
    try:
      _ = select((t, t.book_ref) for t in Ticket).order_by(Ticket.ticket_no).first()
    except Exception:
      pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 7. Nested find first\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  main()