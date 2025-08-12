from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pyodbc
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow all origins for testing (narrow this in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use your frontend domain here later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JSON_FILE = "../data/aircraft.json"
SERVER = "sdr-flight-mapping-sql.database.windows.net,1433;"
DATABASE = "flightdata"
USER = "flighttracker"

#set the environment variable FLIGHTDB_PASSWORD in your .env file
# or export it in your shell before running this script
PASSWORD = os.environ.get("FLIGHTDB_PASSWORD") 

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=" + SERVER +
    "DATABASE=" + DATABASE + ";"
    "UID=" + USER + ";"
    "PWD=" + PASSWORD + ";"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

@app.get("/api/flights")
def get_all_flights():
    try:
        print(connection_string)
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Hex, Flight, Lat, Lon, Altitude, GroundSpeed, Track, Seen, BatchTimeUtc
            FROM AdsbAircraftData
            WHERE BatchTimeUtc = (
                SELECT MAX(BatchTimeUtc) FROM AdsbAircraftData
            )
            AND Lat IS NOT NULL AND Lon IS NOT NULL
            ORDER BY Id
""")

        rows = cursor.fetchall()
        print(f"Retrieved {len(rows)} rows from database.")

        results = []
        for row in rows:
            results.append({
                "hex": row.Hex,
                "flight": row.Flight,
                "lat": row.Lat,
                "lon": row.Lon,
                "altitude": row.Altitude,
                "gs": row.GroundSpeed,
                "track": row.Track,
                "seen": row.Seen,
                "timestamp": row.BatchTimeUtc.isoformat()
            })

        return {"flights": results}

    except Exception as e:
        print(f"Database error: {e}")
        return {"error": str(e)}