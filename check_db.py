import sqlite3

conn = sqlite3.connect("mobile_legends_register_form.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM registrations")
rows = cursor.fetchall()

conn.close()

print(rows)  # Should print registered users
