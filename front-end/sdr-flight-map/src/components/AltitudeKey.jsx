// components/AltitudeLegend.jsx
import React from "react";

const ranges = [
  { label: "< 5,000 ft", icon: "/icons/plane-grey.svg", min: null, max: 5000 },
  { label: "5,000–9,999 ft", icon: "/icons/plane-purple.svg", min: 5000, max: 10000 },
  { label: "10,000–19,999 ft", icon: "/icons/plane-blue.svg", min: 10000, max: 20000 },
  { label: "≥ 20,000 ft", icon: "/icons/plane-green.svg", min: 20000, max: null },
];

function AltitudeKey() {
  return (
    <div className="legend-card">
      <div className="legend-title">Altitude Key</div>
      <ul className="legend-list">
        {ranges.map((r) => (
          <li key={r.label} className="legend-item">
            <img src={r.icon} alt={r.label} className="legend-icon" />
            <span>{r.label}</span>
          </li>
        ))}
      </ul>
      <div className="legend-note">
        Marker color is determined by current altitude (ft).
      </div>
    </div>
  );
}

export default AltitudeKey;
