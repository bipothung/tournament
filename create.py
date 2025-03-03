import sqlite3
conn1 = sqlite3.connect("mobile_legends_register_form.db")
cursor1 = conn1.cursor()
cursor1.execute("""
CREATE TABLE registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    squad_name TEXT NOT NULL,
    squad_id TEXT NOT NULL,
    phone TEXT NOT NULL,
    state TEXT NOT NULL,
    event_name TEXT NOT NULL,
    registration_time TEXT NOT NULL
    );
""")
conn1.commit()
conn1.close()
print("Created successfully")

conn2 = sqlite3.connect("mobile_legends_form_data.db")
cursor2 = conn2.cursor()
cursor2.execute("""
CREATE TABLE IF NOT EXISTS cards(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Card_Head TEXT NOT NULL,
    Card_Para TEXT NOT NULL,
    Modal_Para TEXT NOT NULL
    )
""")
conn2.commit()
conn2.close()
print("Created successfully")