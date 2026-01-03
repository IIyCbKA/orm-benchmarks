import os

COUNT = int(os.environ.get('ITERATIONS', '2500'))

def main() -> None:
  print(
    f'PonyORM. Test 3. Bulk create. {COUNT} entities\n'
    f'Bulk create is not supported'
  )


if __name__ == '__main__':
  main()
