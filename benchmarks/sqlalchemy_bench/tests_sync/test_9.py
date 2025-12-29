import time
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from tests_sync.db import SessionLocal
from core.models import Booking, Ticket


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def main() -> None:
    start = time.perf_counter_ns()

    try:
        with SessionLocal() as session:
            stmt = select(Ticket).where(Ticket.book_ref == generate_book_ref(1))
            result = session.scalars(stmt)
            tickets = [t for t in result]
    except Exception as e:
        print(e)

    elapsed = time.perf_counter_ns() - start

    print(
        f'SQLAlchemy. Test 9. Nested find unique\n'
        f'elapsed_ns={elapsed:.0f};'
    )


if __name__ == '__main__':
    main()
