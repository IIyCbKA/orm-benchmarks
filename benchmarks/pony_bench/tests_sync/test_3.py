import os

COUNT = int(os.environ.get('ITERATIONS', '2500'))

def main() -> None:
  print(
    f"PonyORM. Test 3. Bulk create. {COUNT} entities\n"
    f"Don't have bulk create;"
  )


if __name__ == '__main__':
  main()
