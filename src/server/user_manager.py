import sqlite3
from datetime import date

DB_PATH = "users.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ip TEXT UNIQUE,
                 total_generations INTEGER DEFAULT 0,
                 daily_generations INTEGER DEFAULT 0,
                 last_access DATE)""")
    conn.commit()
    conn.close()

async def register_user(ip: str):
    today = str(date.today())
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE ip=?", (ip,)).fetchone()

    if user is None:
        conn.execute("INSERT INTO users (ip, total_generations, daily_generations, last_access) VALUES (?, 0, 0, ?)", (ip, today))
    else:
        if user["last_access"] != today:
            conn.execute("UPDATE users SET daily_generations=0, last_access=? WHERE ip=?", (today, ip))
    conn.commit()
    conn.close()

def add_generation(ip: str):
    conn = get_db()
    conn.execute("UPDATE users SET total_generations=total_generations+1, daily_generations=daily_generations+1 WHERE ip=?", (ip,))
    conn.commit
    conn.close()

def check_limit(ip: str, daily_limit: int = 5) -> bool:
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE ip=?", (ip,)).fetchone()
    conn.close()
    if user and user["daily_generations"] < daily_limit:
        return True
    return False

def get_stats():
    conn = get_db()
    total_users = conn.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
    month_users = conn.execute("SELECT COUNT(*) as c FROM users WHERE strftime('%Y-%m', last_access) = strftime('%Y-%m', date('now'))").fetchone()["c"]
    conn.close()
    return {"unic_people": total_users, "month_users": month_users}

if __name__ == "__main__":
    init_db()
    print("DATABASE GENERATED")