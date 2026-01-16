from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import statistics
import sys
import time
from tests_sync.db import conn

ITERATION_COUNT = int(os.environ.get('ITERATIONS', '2500'))
NESTED_COUNT = int(os.environ.get('NESTED_COUNT', '5'))


def generate_book_ref(i: int) -> str:
    return f'd{i:05d}'


def generate_ticket_no(i: int, j: int) -> str:
    return f'98{j:04d}{i:07d}'


def generate_passenger_id(i: int) -> str:
    return f'p{i:08d}'


def generate_amount(i: int) -> Decimal:
    value = i + 500
    return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


def create_iteration(i: int) -> int:
    start = time.perf_counter_ns()

    with conn.cursor() as cur:
        book_ref = generate_book_ref(i)
        with conn.transaction():
            cur.execute("""
                INSERT INTO bookings.bookings (book_ref, book_date, total_amount)
                VALUES (%s, %s, %s)
            """, (book_ref, get_curr_date(), generate_amount(i)))

            for j in range(NESTED_COUNT):
                cur.execute("""
                    INSERT INTO bookings.tickets
                    (ticket_no, book_ref, passenger_id, passenger_name, outbound)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    generate_ticket_no(i, j),
                    book_ref,
                    generate_passenger_id(i),
                    'Test',
                    True,
                ))

    end = time.perf_counter_ns()
    return end - start


def main() -> None:
    results: list[int] = []

    try:
        for i in range(ITERATION_COUNT):
            results.append(create_iteration(i))
    except Exception as e:
        print(f'[ERROR] Test 4 failed: {e}')
        sys.exit(1)

    elapsed = statistics.median(results)

    print(
        f'Pure SQL (psycopg3). Test 4. Nested create\n'
        f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
    main()