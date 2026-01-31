import sqlite3

db_path = r"C:\Users\alber\CascadeProjects\pltm-mcp\pltm_mcp.db"
conn = sqlite3.connect(db_path)

# Count atoms
cursor = conn.execute("SELECT COUNT(*) FROM atoms")
total = cursor.fetchone()[0]
print(f"Total atoms: {total}")

# Count by graph
cursor = conn.execute("SELECT graph, COUNT(*) FROM atoms GROUP BY graph")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# Show all atoms
cursor = conn.execute("SELECT subject, predicate, object, graph FROM atoms")
atoms = cursor.fetchall()
print(f"\nAll atoms:")
for atom in atoms:
    print(f"  [{atom[0]}] {atom[1]} → {atom[2]} (graph: {atom[3]})")

# Count distinct predicates
cursor = conn.execute("SELECT COUNT(DISTINCT predicate) FROM atoms WHERE graph = 'substantiated'")
predicates = cursor.fetchone()[0]
print(f"\nDistinct predicates in substantiated graph: {predicates}")

conn.close()
