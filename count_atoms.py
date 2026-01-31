import sqlite3

conn = sqlite3.connect('C:/Users/alber/CascadeProjects/pltm-mcp/pltm_mcp.db')

cursor = conn.execute('SELECT COUNT(*) FROM atoms WHERE graph = ?', ('substantiated',))
total = cursor.fetchone()[0]
print(f'Substantiated atoms: {total}')

cursor = conn.execute('SELECT COUNT(DISTINCT predicate) FROM atoms WHERE graph = ?', ('substantiated',))
predicates = cursor.fetchone()[0]
print(f'Distinct predicates: {predicates}')

conn.close()
