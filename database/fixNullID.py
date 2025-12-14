import sqlite3
import uuid

# Connect to database
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Get all tasks with NULL IDs
cursor.execute('SELECT rowid, title FROM tasks WHERE id IS NULL')
null_rows = cursor.fetchall()

if not null_rows:
    print("✅ No NULL IDs found!")
else:
    print(f"Found {len(null_rows)} tasks with NULL IDs\n")
    
    for i, (rowid, title) in enumerate(null_rows, 1):
        new_uuid = str(uuid.uuid4())
        cursor.execute('UPDATE tasks SET id = ? WHERE rowid = ?', (new_uuid, rowid))
        
        # Show progress
        title_preview = title[:35] + '...' if len(title) > 35 else title
        print(f"[{i}/{len(null_rows)}] {title_preview:40} → {new_uuid}")
    
    conn.commit()
    print(f"\n✅ Successfully fixed {len(null_rows)} tasks!")

conn.close()