from decimal import Decimal
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from tests_sync.db import SessionLocal
from core.models import Booking, Ticket
import os
import statistics
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def main() -> None:
    with SessionLocal() as session:
        try:
            refs = [generate_book_ref(i) for i in range(COUNT)]
            statement = (select(Booking).where(Booking.book_ref.in_(refs)))
            bookings = session.execute(statement).scalars().all()
            session.commit()
        except Exception as e:
            print(f'[ERROR] Test 13 failed (data preparation): {e}')
            sys.exit(1)

        results: list[int] = []

        try:
            for booking in bookings:
                start = time.perf_counter_ns()

                with session.begin():
                    booking.total_amount += Decimal('10.00')
                    stmt = update(Ticket).where(
                        Ticket.book_ref == booking.book_ref).values(
                        passenger_name='Nested update'
                    )
                    session.execute(stmt)

                end = time.perf_counter_ns()
                results.append(end - start)
        except Exception as e:
            print(f'[ERROR] Test 13 failed (delete phase): {e}')
            sys.exit(1)

        elapsed = statistics.median(results)

        print(
            f"SQLAlchemy (sync). Test 13. Nested update\n"
            f"elapsed_ns={elapsed}"
        )


if __name__ == '__main__':
    main()
