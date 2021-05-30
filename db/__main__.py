import argparse
from sqlalchemy import create_engine
import schema

engine = create_engine("postgresql://dmitryk@localhost:5432/postgres")

parser = argparse.ArgumentParser()
parser.add_argument("init", help="This will create standard tables and fields in database (if not exists)")
args = parser.parse_args()

if args.init == "init":
    schema.fill_db()
    print("Tables was created")
else:
    print("Nothing")

