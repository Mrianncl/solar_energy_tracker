# app/stats.py
import sqlite3
from utils.db_utils import DB_PATH

def get_aggregated_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Group by user type
    c.execute('''
        SELECT 
            u.type,
            AVG(s.monthly_saving) as avg_monthly_saving,
            AVG(s.co2_saved_yearly) as avg_co2_saved,
            AVG(s.trees_saved) as avg_trees_saved,
            COUNT(DISTINCT u.id) as total_users
        FROM users u
        JOIN stats s ON u.id = s.user_id
        GROUP BY u.type
    ''')

    rows = c.fetchall()
    conn.close()

    result = {
        "Solar": {"users": 0, "avg_monthly_saving": 0, "avg_co2_saved": 0, "avg_trees_saved": 0},
        "Non-solar": {"users": 0, "avg_monthly_saving": 0, "avg_co2_saved": 0, "avg_trees_saved": 0}
    }

    for row in rows:
        user_type = row[0]
        result[user_type]["users"] = row[4]
        result[user_type]["avg_monthly_saving"] = round(row[1] or 0, 2)
        result[user_type]["avg_co2_saved"] = round(row[2] or 0, 2)
        result[user_type]["avg_trees_saved"] = round(row[3] or 0, 2)

    return result