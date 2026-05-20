import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";

/**
 * Helper to extract a readable title from a stream URL.
 * Uses the pathname (last segment) without extension as fallback.
 */
function deriveTitle(url) {
  try {
    const { hostname, pathname } = new URL(url);
    const name = pathname.split("/").filter(Boolean).pop() || "";
    const cleanName = name.replace(/\.[^/.]+$/, ""); // strip extension
    return `${hostname}/${cleanName}`;
  } catch {
    return url;
  }
}

/**
 * Formats seconds into mm:ss.
 */
function formatDuration(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60)
    .toString()
    .padStart(2, "0");
  return `${mins}:${secs}`;
}

/**
 * RecordingList component – displays a list of recorded episodes.
 *
 * Expected recording shape:
 * {
 *   id: string,
 *   url: string,
 *   duration: number, // seconds
 *   status: string,
 *   createdAt: string // ISO timestamp
 * }
 */
export default function RecordingList() {
  const [recordings, setRecordings] = useState([]);
  const [playingId, setPlayingId] = useState(null);

  // Fetch recordings on mount
  useEffect(() => {
    async function fetchRecordings() {
      try {
        const resp = await fetch("/api/recordings");
        if (!resp.ok) throw new Error("Network response was not ok");
        const data = await resp.json();
        // Sort by most recent (createdAt descending)
        data.sort(
          (a, b) => new Date(b.createdAt) - new Date(a.createdAt)
        );
        setRecordings(data);
      } catch (err) {
        console.error("Failed to load recordings:", err);
      }
    }
    fetchRecordings();
  }, []);

  const handleDelete = async (id) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this recording?"
    );
    if (!confirmed) return;

    try {
      const resp = await fetch(`/api/recordings/${id}`, {
        method: "DELETE",
      });
      if (!resp.ok) throw new Error("Delete failed");
      setRecordings((prev) => prev.filter((rec) => rec.id !== id));
    } catch (err) {
      console.error(err);
      alert("Failed to delete recording.");
    }
  };

  const togglePlay = (id) => {
    setPlayingId((prev) => (prev === id ? null : id));
  };

  return (
    <div className="recording-list">
      {recordings.length === 0 ? (
        <p>No recordings found.</p>
      ) : (
        <ul>
          {recordings.map((rec) => (
            <li key={rec.id} className="recording-item">
              <div
                className="recording-info"
                onClick={() => togglePlay(rec.id)}
                style={{ cursor: "pointer" }}
                data-testid={`recording-${rec.id}`}
              >
                <strong>{deriveTitle(rec.url)}</strong>
                <span>Duration: {formatDuration(rec.duration)}</span>
                <span>Status: {rec.status}</span>
              </div>
              <button
                onClick={() => handleDelete(rec.id)}
                className="delete-button"
                data-testid={`delete-${rec.id}`}
              >
                Delete
              </button>
              {playingId === rec.id && (
                <audio
                  src={rec.url}
                  controls
                  autoPlay
                  data-testid={`audio-${rec.id}`}
                />
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

RecordingList.propTypes = {
  // No external props; component fetches its own data.
};