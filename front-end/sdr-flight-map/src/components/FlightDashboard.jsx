// pages/FlightDashboard.jsx
import AboutImpact from "./AboutImpact";
import FlightMap from "./FlightMap"; 
import GitHubRepo from "./GitHubRepo";
import AltitudeKey from "./AltitudeKey";
import "../index.css";

export default function FlightDashboard() {
  return (
    <div className="wrap">
      <div className="map-col">
        <FlightMap /> 
      </div>

      <aside className="side-col">
        <div className="side-inner">
          <AboutImpact />
          <GitHubRepo url="https://github.com/kavanainamdar/sdr-flight-mapping" />
          <AltitudeKey />
        </div>
      </aside>
    </div>
  );
}
