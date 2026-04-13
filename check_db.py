import sqlite3
import os

# Check database
db_path = "d:/Quan_Ho/quan_ho.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check users
    cursor.execute("SELECT id, name, email, role FROM users")
    users = cursor.fetchall()
    print("Users in database:")
    for user in users:
        print(f"  ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Role: {user[3]}")
    
    # Check events
    cursor.execute("SELECT id, title FROM events")
    events = cursor.fetchall()
    print("\nEvents in database:")
    for event in events:
        print(f"  ID: {event[0]}, Title: {event[1]}")
    
    conn.close()
else:
    print("Database not found")
