import sqlite3
from pathlib import Path
from app.data.db import *
from app.data.schema import *
from app.data.users import *
from app.data.cyber_incidents import *
from app.data.datasets import *
from app.data.tickets import *


# Database connection
conn = connect_database(DB_PATH)

# Create users table
create_users_table(conn)

# Migrate users
migrate_users_from_file(conn, DATA_TXT)

# Migrate cyber incidents
load_csv_to_table(conn)

# Migrate metadata
load_dataset_csv(conn)

# Migrate tickets
load_ticket_csv(conn)