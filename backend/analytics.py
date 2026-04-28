import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "analytics.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                query TEXT,
                route TEXT,
                used_web INTEGER DEFAULT 0,
                response_time REAL,
                timestamp TEXT
            )
        """)
        conn.commit()

def log_query(session_id: str, query: str, route: str, used_web: bool, response_time: float):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO queries (session_id, query, route, used_web, response_time, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (session_id, query, route, int(used_web), response_time, datetime.utcnow().isoformat()))
        conn.commit()

def get_stats():
    with sqlite3.connect(DB_PATH) as conn:
        total = conn.execute("SELECT COUNT(*) FROM queries").fetchone()[0]
        rag_hits = conn.execute("SELECT COUNT(*) FROM queries WHERE route='rag_lookup'").fetchone()[0]
        web_hits = conn.execute("SELECT COUNT(*) FROM queries WHERE used_web=1").fetchone()[0]
        avg_time = conn.execute("SELECT AVG(response_time) FROM queries").fetchone()[0]
        recent = conn.execute("""
            SELECT query, route, used_web, response_time, timestamp 
            FROM queries ORDER BY id DESC LIMIT 10
        """).fetchall()
    return {
        "total_queries": total,
        "rag_hits": rag_hits,
        "web_hits": web_hits,
        "avg_response_time": round(avg_time or 0, 2),
        "recent_queries": recent
    }

init_db()