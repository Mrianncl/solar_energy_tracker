

# app/input_handler.py
import sqlite3
from datetime import date

def validate_numeric(value, field_name):
    try:
        if value.strip() == "":
            raise ValueError(f"{field_name} cannot be empty.")
        return float(value)
    except ValueError:
        raise ValueError(f"Invalid numeric value for {field_name}")

def save_user_input(data, user_id=None):
    conn = sqlite3.connect("../data/users.db")
    c = conn.cursor()

    if user_id is None:
        user_id = 1  # fallback only if no user logged in

    monthly_saving = data.get("monthly_saving", 0)
    co2_saved_yearly = data.get("co2_yearly", 0)
    trees_saved = data.get("trees_saved", 0)

    c.execute('''
        INSERT INTO stats (user_id, monthly_saving, co2_saved_yearly, trees_saved, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, monthly_saving, co2_saved_yearly, trees_saved, str(date.today())))

    conn.commit()
    conn.close()
    return True
    # print("User Input Saved:", data)