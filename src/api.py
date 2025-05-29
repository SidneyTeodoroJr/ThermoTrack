from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import List
from pydantic import BaseModel
import logging
import os

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = os.path.join("assets", "data", "data-base.db")

class Record(BaseModel):
    datetime: str
    temperature: float
    efficiency: float

@app.on_event("startup")
def startup():
    # Ensure the folder exists
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    # Create the table if it doesn't exist
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS records (
        datetime TEXT PRIMARY KEY,
        temperature REAL NOT NULL,
        efficiency REAL NOT NULL
    )
    """)
    conn.commit()
    cur.close()
    conn.close()
    logging.info("Database initialized and table created if not exists.")

@app.get("/history", response_model=List[Record])
def get_history():
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT datetime, temperature, efficiency FROM records ORDER BY datetime")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [
            Record(datetime=row[0], temperature=row[1], efficiency=row[2])
            for row in rows
        ]
    except Exception as e:
        logging.error(f"Error fetching history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch history")

@app.get("/latest", response_model=Record)
def get_latest_record():
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT datetime, temperature, efficiency FROM records ORDER BY datetime DESC LIMIT 1")
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            return Record(datetime=row[0], temperature=row[1], efficiency=row[2])
        else:
            raise HTTPException(status_code=404, detail="No data found")

    except Exception as e:
        logging.error(f"Error fetching latest record: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch latest record")

@app.post("/records")
def create_record(record: Record):
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO records (datetime, temperature, efficiency) VALUES (?, ?, ?)",
            (record.datetime, record.temperature, record.efficiency)
        )
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Record inserted successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Record with this datetime already exists")
    except Exception as e:
        logging.error(f"Error inserting record: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to insert record: {e}")