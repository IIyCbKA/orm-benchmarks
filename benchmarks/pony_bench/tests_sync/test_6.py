from pony.orm import db_session
from core.models import Booking
import time

def main() -> None:
  start = time.time()

  with db_session():
    try:
        _ = Booking.select.first()
    except Exception:
      pass

  end = time.time()
  elapsed = end - start

  print(
    f'PonyORM. Test 6. Find first\n'
    f'elapsed_sec={elapsed:.4f};'
  )


if __name__ == '__main__':
  main()