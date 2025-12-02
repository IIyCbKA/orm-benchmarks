ORM & SQL Performance Bench [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/IIyCbKA/sql-orm-benchmarks/blob/main/LICENSE) [![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/downloads/release/python-3120/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/)
==============

A reproducible benchmarking project to compare raw SQL and popular Python ORMs on PostgreSQL.

The primary database schema used in this project is the demonstration schema 
provided by Postgres Professional: https://postgrespro.ru/education/demodb. 
For reproducibility, each benchmark run is initialized from the one-year dump 
`demo-20250901-1y.sql.gz`, available at 
https://edu.postgrespro.ru/demo-20250901-1y.sql.gz. The dump is restored 
immediately prior to testing so that every run starts from the same dataset. 

For stability the dump has been incorporated into the database image and 
published on Docker Hub at: 
https://hub.docker.com/repository/docker/iiycbka/sql-orm-benchmarks-db.

---

### Running

**IMPORTANT NOTE:** On each fresh run of `docker-compose` you must clear all 
volumes and any references from previous runs.

The easiest way to bring up a solution is (example):
```bash
# from repo root
./start.sh <solution>

# stop and remove containers, networks and declared volumes
./stop.sh <solution>
```

**IMPORTANT NOTE:** In the Docker Compose setup we use a special healthcheck 
for the database container. It is included in the same image as the database 
dump and is designed to verify the existence of all tables defined in the 
database schema shown above. In other words, the check will only pass once 
every table in the schema has been created.

### Viewing benchmark results

Each benchmark prints its result to stdout. These stdout lines are captured 
by Docker and can be viewed via the runner container logs.

From the repository root, after starting a solution (e.g. `./start.sh pony`), 
view live output with the helper script:

```bash
# follow live runner logs for solution
./logs.sh <solution>
```

You can also run the equivalent directly:
```bash
# with modern docker
docker compose -f <path_to_compose>/docker-compose.yaml logs -f runner

# or with older docker-compose
docker-compose -f <path_to_compose>/docker-compose.yaml logs -f runner
```

List of existing solutions available for start/stop/logs (use the solution 
name from this list in `./start.sh`, `./stop.sh` and `./logs.sh`):
- pony
- sqlalchemy

For convenience, ready-to-use start.sh, stop.sh and logs.sh scripts are 
included in the repository root. Simply run them from the repo root and pass 
the solution name.

---

### Tests:

1. Insert: Single (single entry at a time)
2. Insert: Batch (many bathed in transaction)
3. Insert: Bulk (bulk insert operation)
4. Filter: Large (large result set)
---

Stack: Python 3.12, PostgreSQL.\
ORMs included: Pony ORM, Django ORM, SQLAlchemy, Tortoise ORM — plus raw SQL baseline.\
Authors: student research team.\
License: MIT.