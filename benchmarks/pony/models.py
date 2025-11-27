from dotenv import load_dotenv
from pony.orm import Database
import os

load_dotenv()

db = Database()

db.bind(
  provider='postgres',
  user=os.environ.get('POSTGRES_USER', 'postgres'),
  password=os.environ.get('POSTGRES_PASSWORD', ''),
  host=os.environ.get('POSTGRES_HOST', 'localhost'),
  db=os.environ.get('POSTGRES_DB', 'postgres'),
)

db.generate_mapping(create_tables=False)