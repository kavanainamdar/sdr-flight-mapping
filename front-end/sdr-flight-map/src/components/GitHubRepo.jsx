// components/GitHubRepo.jsx
import React from "react";

export default function GitHubRepo({ url = "https://github.com/kavanainamdar/sdr-flight-mapping" }) {
  return (
    <section className="panel-section">
      <h2 className="panel-heading">GitHub Repository</h2>
      <a
        href={url}
        target="_blank"
        rel="noreferrer"
        className="repo-link"
        title="Open repository"
      >
        {url}
      </a>
    </section>
  );
}
