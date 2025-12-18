import time

import django
django.setup()

from core.models import Booking

def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def main() -> None:
  start = time.time()

  try:
    _ = Booking.objects.filter(book_ref=generate_book_ref(1)).first()
  except Exception:
    pass

  end = time.time()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 8. Find unique\n'
    f'elapsed_sec={elapsed:.4f};'
  )


if __name__ == '__main__':
  main()
