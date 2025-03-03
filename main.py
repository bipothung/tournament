from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Database connection function
def get_db_connection(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

# Ensure the required tables exist
def create_tables():
    conn = get_db_connection("mobile_legends_register_form.db")
    cursor = conn.cursor()

    # Create the registrations table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        squad_name TEXT NOT NULL,
        squad_id TEXT NOT NULL,
        phone TEXT NOT NULL,
        state TEXT NOT NULL,
        event_name TEXT NOT NULL,
        registration_time TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# Insert event card if it doesn't exist
def insert_card_if_not_exists():
    conn = get_db_connection("mobile_legends_form_data.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Card_Head TEXT,
        Card_Para TEXT,
        Modal_Para TEXT
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM cards WHERE Card_Head = ?", ("Squad Showdown: Season 1",))
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("""
        INSERT INTO cards (Card_Head, Card_Para, Modal_Para) 
        VALUES (?, ?, ?)
        """, ("Squad Showdown: Season 1",
              "Game: Mobile Legends, Game Type: Squad Vs Squad, Registration Fee: ₹300, First Winning Prize: ₹1300, Second Winning Prize: ₹700",
              """
              Join the ultimate battle and prove your skills in this thrilling tournament with exciting cash prizes! The tournament features Mobile Legends in a Squad vs Squad format, with a registration fee of ₹300 per squad and the first winning prize will be ₹1400 and second prize will be ₹700 (paid via GPay). The registration is open now, it will close on _th March. Matches will be held online, allowing players to compete from home. The knockout format includes 8 squads battling in three rounds, with the match starting at 09:00AM on _th March. Prize money will be transferred to the winner's GPay number, and further details will be shared via WhatsApp upon registration. Are you ready for the challenge? Register now and dominate the battlefield!
              """))
        conn.commit()

    conn.close()

# Initialize tables and insert event details
create_tables()
insert_card_if_not_exists()

@app.route("/")
def index():
    conn = get_db_connection("mobile_legends_form_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cards")
    cards = cursor.fetchall()
    conn.close()
    return render_template("index.html", cards=cards if cards else None)

@app.route("/view_matches")
def view_matches():
    return render_template("view_matches.html")

@app.route("/about_me")
def about_me():
    return render_template("about_me.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    print("Received data:", data)  # Debugging line to check incoming request

    if not data:
        return jsonify({"success": False, "message": "No data received"}), 400  # Handle empty request

    name = data.get("name")
    email = data.get("email")
    squad_name = data.get("squad_name")
    squad_id = data.get("squad_id")
    phone = data.get("phone")
    state = data.get("state")
    event_name = data.get("event_name")
    registration_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    try:
        conn = get_db_connection("mobile_legends_register_form.db")
        cursor = conn.cursor()

        # Check if the user is already registered using email or phone
        cursor.execute("SELECT COUNT(*) FROM registrations WHERE (email = ? OR phone = ?) AND event_name = ?", (email, phone, event_name))
        count = cursor.fetchone()[0]

        if count > 0:
            conn.close()
            return jsonify({"success": False, "message": "You are already registered for this event."})

        # Check if event registration limit is reached
        cursor.execute("SELECT COUNT(*) FROM registrations WHERE event_name = ?", (event_name,))
        count = cursor.fetchone()[0]

        if count >= 8:
            conn.close()
            return jsonify({"success": False, "message": "Registration full for this event. Try another event."})

        # Insert new registration and print query
        insert_query = """
        INSERT INTO registrations (name, email, squad_name, squad_id, phone, state, event_name, registration_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        print("Executing SQL:", insert_query, (name, email, squad_name, squad_id, phone, state, event_name, registration_time))

        cursor.execute(insert_query, (name, email, squad_name, squad_id, phone, state, event_name, registration_time))
        conn.commit()
        print("Data committed successfully!")

        conn.close()
        return jsonify({"success": True, "message": "Registration successful! We will contact you on WhatsApp shortly."})

    except sqlite3.Error as e:
        print(f"Database error: {e}")  # Debugging line to catch database errors
        return jsonify({"success": False, "message": f"Database error: {e}"})
    except Exception as e:
        print(f"Unexpected error: {e}")  # Debugging line to catch unexpected errors
        return jsonify({"success": False, "message": f"Unexpected error: {e}"})

# Route to view registered users (for debugging)
@app.route("/registrations", methods=["GET"])
def view_registrations():
    try:
        conn = get_db_connection("mobile_legends_register_form.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registrations")
        registrations = cursor.fetchall()
        conn.close()

        print("Fetched registrations from DB:", registrations)  # Debugging line

        if not registrations:
            return jsonify({"success": False, "message": "No registrations found."})

        data = [dict(row) for row in registrations]  # This might be causing issues
        print("Converted data for API response:", data)  # Debugging line

        return jsonify({"success": True, "registrations": data})

    except sqlite3.Error as e:
        return jsonify({"success": False, "message": f"Database error: {e}"})

# Run the Flask app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT from Render or default to 5000
    app.run(host="0.0.0.0", port=port)
