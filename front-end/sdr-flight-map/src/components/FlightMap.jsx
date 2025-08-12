import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "../index.css";

// Function to return an icon based on altitude
const getFlightIcon = (altitude) => {
  let iconUrl = ""; 
  if (altitude < 5000) {
  iconUrl = "/icons/plane-grey.svg";
} else if (altitude >= 5000 && altitude < 10000) {
  iconUrl = "/icons/plane-purple.svg";
} else if (altitude >= 10000 && altitude < 20000) {
  iconUrl = "/icons/plane-blue.svg";
} else if (altitude >= 20000) {
  iconUrl = "/icons/plane-green.svg";
}


  return new L.Icon({
    iconUrl,
    iconSize: [50, 50],
    iconAnchor: [16, 16],
    popupAnchor: [0, -16],
  });
};

function FlightMap() {
  const [flights, setFlights] = useState([]);

  useEffect(() => {
    const fetchFlights = async () => {
      try {
        // Fetch flight data from the API
        const res = await fetch("https://sdr-flight-mapping-api.azurewebsites.net/api/flights");
        const json = await res.json();
        setFlights(json.flights || []);
      } catch (err) {
        console.error("Error fetching flights:", err);
      }
    };

    fetchFlights();
    const interval = setInterval(fetchFlights, 10000);
    return () => clearInterval(interval);
  }, []);

  const validFlights = flights.filter(
    (f) => typeof f.lat === "number" && typeof f.lon === "number"
  );

  return (
    <MapContainer
      center={[47.6, -122.3]}
      zoom={10}
      style={{ height: "100vh", width: "100%" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {validFlights.map((flight, idx) => (
        <Marker
          key={idx}
          position={[flight.lat, flight.lon]}
          icon={getFlightIcon(flight.altitude || 0)}
        >
          <Popup>
            <strong>{flight.flight || "Unknown flight"}</strong>
            <br />
            Altitude: {flight.altitude || "N/A"} ft
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default FlightMap;
