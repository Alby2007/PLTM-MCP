import sqlite3

db_path = r"C:\Users\alber\CascadeProjects\LLTM\mcp_server\pltm_mcp.db"
conn = sqlite3.connect(db_path)

# List tables
cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print(f"Tables: {tables}")

# Count atoms in each table
for table in tables:
    try:
        cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table}: {count} rows")
    except Exception as e:
        print(f"{table}: Error - {e}")

# If atoms table exists, show sample
if 'atoms' in tables:
    cursor = conn.execute("SELECT * FROM atoms LIMIT 3")
    rows = cursor.fetchall()
    if rows:
        print(f"\nSample atoms:")
        for row in rows:
            print(f"  {row[:5]}...")  # First 5 columns
    else:
        print("\nAtoms table is empty")

conn.close()
