from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import session_user
from tests_sync.db import SessionLocal
from core.models import Booking, Ticket
import os
import statistics
import sys
import time

SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def select_iteration() -> int:
    start = time.perf_counter_ns()

    session = SessionLocal()
    stmt = (
        select(
            Ticket.ticket_no,
            Ticket.book_ref,
            Ticket.passenger_id,
            Ticket.passenger_name,
            Ticket.outbound,
            Booking.book_ref,
            Booking.book_date,
            Booking.total_amount,
        )
        .join(Booking, Ticket.book_ref == Booking.book_ref)
        .where(Ticket.book_ref == generate_book_ref(1))
    )
    _ = session.scalars(stmt).all()

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
        f'SQLAlchemy (sync). Test 9. Nested find\n'
        f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
    main()
