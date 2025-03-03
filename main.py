from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

card_head = "Squad Showdown: Season 1"
card_para = "Game: Mobile Legends, Game Type: Squad Vs Squad, Registration Fee: ₹300, First Winning Prize: ₹1300, Second Winning Prize: ₹700"
modal_para = """
        Join the ultimate battle and prove your skills in this thrilling tournament with exciting cash prizes! The tournament features Mobile Legends in a Squad vs Squad format, with a registration fee of ₹300 per squad and the first winning prize will be ₹1400 and second prize will be ₹700 (paid via GPay). The registration is open now, it will close on _th March. Matches will be held online, allowing players to compete from home. The knockout format includes 8 squads battling in three rounds, with the match starting at 09:00AM on _th March. Prize money will be transferred to the winner's GPay number, and further details will be shared via WhatsApp upon registration. Are you ready for the challenge? Register now and dominate the battlefield!
"""
        
def insert_card_if_not_exists():
    conn = get_db_connection("mobile_legends_form_data.db")
    cursor = conn.cursor()

    # Check if the card already exists
    cursor.execute("SELECT COUNT(*) FROM cards WHERE Card_Head = ?", (card_head,))
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("""
        INSERT INTO cards (Card_Head, Card_Para, Modal_Para) 
        VALUES (?, ?, ?)
        """, (card_head, card_para, modal_para))
        conn.commit()
    
    conn.close()

insert_card_if_not_exists()

# conn = sqlite3.connect("mobile_legends_register_form.db")
# cursor = conn.cursor()
# cursor.execute("delete from registrations")
# conn.commit()
# conn.close()

@app.route("/")
def index():
    conn = get_db_connection('mobile_legends_form_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cards")
    cards = c.fetchall()
    conn.close()

    # Check if there are any cards
    if not cards:
        return render_template("index.html", cards=None)
    
    return render_template("index.html", cards=cards)

@app.route("/view_matches")
def view_matches():
    return render_template("view_matches.html")

@app.route("/about_me")
def about_me():
    return render_template("about_me.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    squad_name = data['squad_name']
    squad_id = data['squad_id']
    phone = data['phone']
    state = data['state']
    event_name = data['event_name']  # Get dynamic event name from frontend
    registration_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    try:
        conn = get_db_connection('mobile_legends_register_form.db')
        c = conn.cursor()

        # Check if the user is already registered using email or phone
        c.execute("SELECT COUNT(*) FROM registrations WHERE (email = ? OR phone = ?) AND event_name = ?", (email, phone, event_name))
        count = c.fetchone()[0]

        if count > 0:
            conn.close()
            return jsonify({"success": False, "message": "You are already registered for this event."})

        # Check the number of registrations for this event
        c.execute("SELECT COUNT(*) FROM registrations WHERE event_name = ?", (event_name,))
        count = c.fetchone()[0]

        if count >= 8:  # Limit per event
            conn.close()
            return jsonify({"success": False, "message": "Registration full for this event. Try another event."})

        # Insert new registration
        c.execute("INSERT INTO registrations (name, email, squad_name, squad_id, phone, state, event_name, registration_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (name, email, squad_name, squad_id, phone, state, event_name, registration_time))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Registration successful! We will contact you on WhatsApp shortly to confirm your payment and provide more details regarding the match. Thank you for your participation!"})

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({"success": False, "message": "Registration failed due to a database error. Please try again later."})
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"success": False, "message": "Registration failed due to an unexpected error. Please try again later."})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT from Render or default to 5000
    app.run(host="0.0.0.0", port=port)

