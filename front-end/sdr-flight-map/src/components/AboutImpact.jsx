// components/AboutImpact.jsx
import React from "react";

export default function AboutImpact() {
  return (
    <section className="panel-section">
      <h2 className="panel-heading">About Me • Impact</h2>
      <p className="panel-text">
        I’m building a real-time flight tracker using SDR antennas,
        a FastAPI backend, and React + Leaflet for visualization. The goal is to
        make aviation data accessible and educational for students and hobbyists.
        While hidden signals usually are only accesible through specialized tools, I
        wanted to create a public API that makes the data available and also portrays it
        to novice enthusiasts.
      </p>
      <p className="blurb">
        Provides accesible SDR Data representation for wider audiences.
      </p>
    </section>
  );
}
