import sqlite3

DB_NAME = "cases.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        case_id TEXT PRIMARY KEY,
        timestamp TEXT,
        latitude REAL,
        longitude REAL,
        severity INTEGER,
        risk_score REAL,
        region TEXT,
        response TEXT,
        status TEXT,
        image_path TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_case(case_data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, case_data)

    conn.commit()
    conn.close()


def fetch_cases():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cases")
    cases = cursor.fetchall()

    conn.close()
    return cases


def delete_case(case_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cases WHERE case_id = ?", (case_id,))
    conn.commit()
    conn.close()