
import json
import os
import time
import pyodbc
import datetime

print(f"[INFO] Running: {__file__}")

# Path to dump1090-fa output
JSON_FILE = "../data/aircraft.json"
SERVER = "sdr-flight-mapping-sql.database.windows.net,1433;"
DATABASE = "flightdata"
USER = "flighttracker"

#set the environment variable FLIGHTDB_PASSWORD in your .env file
# or export it in your shell before running this script
PASSWORD = os.environ.get("FLIGHTDB_PASSWORD") 

# Azure SQL connection string

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

def read_aircraft_data():
    """
    Read aircraft data from dump1090-fa JSON output.
    :return: List of aircraft dicts.
    """
    try:
        print(f"[INFO] Reading aircraft data from: {JSON_FILE}")
        with open(JSON_FILE, 'r') as f:
            data = json.load(f)
            print(f"[INFO] Loaded {len(data.get('aircraft', []))} aircraft records.")
            return data.get("aircraft", [])
    except FileNotFoundError:
        print(f"[ERROR] File not found: {JSON_FILE}")
        return []
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON decode error: {e}")
        return []

def upload_flight_data(connection_string, data):
    """
    Upload flight data to the database.
    :param connection_string: Azure SQL connection string.
    :param data: List of aircraft dicts from dump1090-fa.
    """
    # Use consistent timestamp for the batch
    batch_time = datetime.datetime.now()
    print(f"[INFO] Uploading flight data to database at {batch_time.strftime('%Y-%m-%d %H:%M:%S')}")
    

    try:
        print("[INFO] Connecting to Azure SQL Database...")
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()

            print("[INFO] Clearing previous data from AdsbAircraftData table...")
            cursor.execute("DELETE FROM AdsbAircraftData")
            print("[INFO] Cleared existing rows.")

            inserted = 0
            for i, flight in enumerate(data, 1):
                lat = flight.get("lat")
                lon = flight.get("lon")

                if lat is None or lon is None:
                    continue  # skip if no position

                cursor.execute("""
                    INSERT INTO AdsbAircraftData (
                        BatchTimeUtc, Hex, Flight, Lat, Lon, Altitude, GroundSpeed, Track, Seen, AircraftJson
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    batch_time,
                    flight.get("hex"),
                    flight.get("flight"),
                    lat,
                    lon,
                    flight.get("alt_geom") or flight.get("alt_baro"),
                    flight.get("gs"),
                    flight.get("track"),
                    flight.get("seen"),
                    json.dumps(flight)
                ))
                print(f"[INFO] Inserted flight {i}: hex={flight.get('hex')}, flight={flight.get('flight')}, lat={lat}, lon={lon}")
                inserted += 1

            conn.commit()
            print(f"[{batch_time.strftime('%Y-%m-%d %H:%M:%S')}] [INFO] Inserted {inserted} valid flights.")

    except Exception as e:
        print(f"[ERROR] Upload error: {e}")


# Loop every 10 seconds
print("[INFO] Starting main loop. Will check for new aircraft data every 10 seconds.")
while True:
    aircraft_data = read_aircraft_data()
    if aircraft_data:
        print(f"[INFO] Found {len(aircraft_data)} aircraft records. Proceeding to upload.")
        upload_flight_data(connection_string, aircraft_data)
    else:
        print(f"[{time.strftime('%X')}] [INFO] No aircraft data found.")
    time.sleep(10)
