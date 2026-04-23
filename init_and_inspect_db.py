import sqlite3
import os

print("=" * 60)
print("DATABASE INITIALIZATION AND INSPECTION")
print("=" * 60)

db_path = "data/scores.db"
print("\nConnecting to: " + db_path)
print("Database file exists: " + str(os.path.exists(db_path)))
print("Database file size: " + str(os.path.getsize(db_path)) + " bytes")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check current tables
print("\n" + "=" * 60)
print("CURRENT TABLES IN DATABASE")
print("=" * 60)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables found: " + str(len(tables)))
for table in tables:
    print("  - " + table[0])

# Create scores table if it doesn't exist
print("\n" + "=" * 60)
print("CREATING SCORES TABLE")
print("=" * 60)
create_table_sql = """
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    score INTEGER,
    total INTEGER,
    percentage REAL,
    categories TEXT,
    question_counts TEXT,
    timer_used INTEGER,
    answers TEXT
)
"""
cursor.execute(create_table_sql)
conn.commit()
print("Scores table created (or already exists)")

# Check tables again after creation
print("\n" + "=" * 60)
print("ALL TABLES IN DATABASE (AFTER CREATION)")
print("=" * 60)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables found: " + str(len(tables)))
for table in tables:
    print("  - " + table[0])

# Get scores table schema
print("\n" + "=" * 60)
print("SCORES TABLE SCHEMA")
print("=" * 60)
cursor.execute("PRAGMA table_info(scores)")
columns = cursor.fetchall()
print("Columns in scores table: " + str(len(columns)))
print("\nColumn Details:")
print("{:<5} {:<20} {:<15} {:<8} {:<10} {:<3}".format("CID", "Name", "Type", "NotNull", "Default", "PK"))
print("-" * 60)
for col in columns:
    cid, name, col_type, notnull, default, pk = col
    print("{:<5} {:<20} {:<15} {:<8} {:<10} {:<3}".format(str(cid), name, col_type, str(notnull), str(default), str(pk)))

# Check data
print("\n" + "=" * 60)
print("DATA STATISTICS")
print("=" * 60)
cursor.execute("SELECT COUNT(*) FROM scores")
row_count = cursor.fetchone()[0]
print("Total rows in scores table: " + str(row_count))

if row_count > 0:
    print("\nFirst row sample:")
    cursor.execute("SELECT * FROM scores LIMIT 1")
    row = cursor.fetchone()
    col_names = [description[0] for description in cursor.description]
    for i, col_name in enumerate(col_names):
        print("  " + col_name + ": " + str(row[i]))
else:
    print("(No data in table yet)")

conn.close()
print("\n" + "=" * 60)
print("DATABASE INSPECTION COMPLETE")
print("=" * 60)
