#!/usr/bin/env python3
"""
Migrate atoms from old LLTM database to new pltm-mcp database.
Old: LLTM/mcp_server/pltm_mcp.db (377 atoms)
New: pltm-mcp/pltm_mcp.db (properly configured with WAL + FULL sync)
"""

import sqlite3
from pathlib import Path

# Database paths
OLD_DB = Path(r"C:\Users\alber\CascadeProjects\LLTM\mcp_server\pltm_mcp.db")
NEW_DB = Path(r"C:\Users\alber\CascadeProjects\pltm-mcp\pltm_mcp.db")

def migrate():
    if not OLD_DB.exists():
        print(f"❌ Old database not found: {OLD_DB}")
        return
    
    print(f"📂 Old DB: {OLD_DB} ({OLD_DB.stat().st_size} bytes)")
    print(f"📂 New DB: {NEW_DB} ({NEW_DB.stat().st_size} bytes)")
    
    # Connect to both databases
    old_conn = sqlite3.connect(str(OLD_DB))
    new_conn = sqlite3.connect(str(NEW_DB))
    
    try:
        # Get all atoms from old database
        old_cursor = old_conn.execute("SELECT * FROM atoms")
        atoms = old_cursor.fetchall()
        
        # Get column names
        columns = [desc[0] for desc in old_cursor.description]
        print(f"\n📊 Found {len(atoms)} atoms in old database")
        print(f"📋 Columns: {', '.join(columns)}")
        
        if not atoms:
            print("⚠️  No atoms to migrate!")
            return
        
        # Insert into new database
        migrated = 0
        skipped = 0
        
        placeholders = ','.join(['?' for _ in columns])
        insert_sql = f"INSERT OR IGNORE INTO atoms ({','.join(columns)}) VALUES ({placeholders})"
        
        for atom in atoms:
            try:
                new_conn.execute(insert_sql, atom)
                migrated += 1
            except Exception as e:
                print(f"⚠️  Error migrating atom: {e}")
                skipped += 1
                continue
        
        # Commit changes
        new_conn.commit()
        
        print(f"\n✅ Migration complete!")
        print(f"   Migrated: {migrated} atoms")
        print(f"   Skipped: {skipped} atoms")
        
        # Verify new database
        new_cursor = new_conn.execute("SELECT COUNT(*) FROM atoms WHERE graph = 'substantiated'")
        total = new_cursor.fetchone()[0]
        print(f"   Total substantiated atoms in new DB: {total}")
        
        # Show some stats
        new_cursor = new_conn.execute("SELECT COUNT(DISTINCT predicate) FROM atoms WHERE graph = 'substantiated'")
        predicates = new_cursor.fetchone()[0]
        print(f"   Distinct predicates: {predicates}")
        
    finally:
        old_conn.close()
        new_conn.close()

if __name__ == "__main__":
    migrate()
