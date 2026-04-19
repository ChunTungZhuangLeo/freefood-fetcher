"""
Free Food Fetcher - Backend Server
Serves the static site and provides a reviews API backed by SQLite.

Run with:
    uvicorn freefood_server:app --reload --port 8080
"""

import sqlite3
import os
from datetime import datetime, timezone
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

DB_PATH = os.path.join(os.path.dirname(__file__), "reviews.db")


# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id  TEXT    NOT NULL,
                author    TEXT    NOT NULL DEFAULT 'Anonymous',
                rating    INTEGER NOT NULL DEFAULT 0,
                text      TEXT    NOT NULL DEFAULT '',
                tags      TEXT    NOT NULL DEFAULT '',
                created_at TEXT   NOT NULL
            )
        """)
        conn.commit()


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


init_db()


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(title="Free Food Fetcher API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class ReviewIn(BaseModel):
    event_id: str
    author: str = "Anonymous"
    rating: int = 0
    text: str = ""
    tags: list[str] = []


class ReviewOut(BaseModel):
    id: int
    event_id: str
    author: str
    rating: int
    text: str
    tags: list[str]
    created_at: str
    timeAgo: str


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def time_ago(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso)
        diff = datetime.now(timezone.utc) - dt
        s = int(diff.total_seconds())
        if s < 60:
            return "just now"
        if s < 3600:
            return f"{s // 60}m ago"
        if s < 86400:
            return f"{s // 3600}h ago"
        return f"{s // 86400}d ago"
    except Exception:
        return ""


def row_to_review(row) -> ReviewOut:
    return ReviewOut(
        id=row["id"],
        event_id=row["event_id"],
        author=row["author"],
        rating=row["rating"],
        text=row["text"],
        tags=[t for t in row["tags"].split("|") if t],
        created_at=row["created_at"],
        timeAgo=time_ago(row["created_at"]),
    )


# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------

@app.get("/api/reviews/{event_id}", response_model=list[ReviewOut])
def get_reviews(event_id: str):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM reviews WHERE event_id = ? ORDER BY id DESC",
            (event_id,)
        ).fetchall()
    return [row_to_review(r) for r in rows]


@app.post("/api/reviews", response_model=ReviewOut)
def post_review(review: ReviewIn):
    if not review.text.strip() and review.rating == 0:
        raise HTTPException(status_code=400, detail="Provide a rating or review text.")
    now = datetime.now(timezone.utc).isoformat()
    tags_str = "|".join(review.tags)
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO reviews (event_id, author, rating, text, tags, created_at) VALUES (?,?,?,?,?,?)",
            (review.event_id, review.author, review.rating, review.text.strip(), tags_str, now)
        )
        conn.commit()
        row = conn.execute("SELECT * FROM reviews WHERE id = ?", (cur.lastrowid,)).fetchone()
    return row_to_review(row)


@app.delete("/api/reviews/{review_id}")
def delete_review(review_id: int):
    with get_db() as conn:
        conn.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
        conn.commit()
    return {"deleted": review_id}


# ---------------------------------------------------------------------------
# Static file serving
# ---------------------------------------------------------------------------

# Serve /data/ directory for events.json
app.mount("/data", StaticFiles(directory="data"), name="data")

# Serve /demo/ directory
app.mount("/demo", StaticFiles(directory="demo"), name="demo")

# Root → redirect to the main demo page
@app.get("/")
def root():
    return FileResponse("demo/freefood-v2.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
