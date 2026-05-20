import React, { useEffect, useState } from "react";

const Dashboard = () => {
  const [data, setData] = useState({
    progress: null,
    upcoming: [],
    preferences: {},
  });
  const [loading, setLoading] = useState(true);
  const [prefInput, setPrefInput] = useState({ language: "", level: "" });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  // Fetch dashboard data on mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const resp = await fetch("/api/dashboard");
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const json = await resp.json();
        setData(json);
      } catch (e) {
        setError(`Failed to load dashboard: ${e.message}`);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handlePrefChange = (e) => {
    const { name, value } = e.target;
    setPrefInput((prev) => ({ ...prev, [name]: value }));
  };

  const handlePrefSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      const resp = await fetch("/api/dashboard/preferences", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(prefInput),
      });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const updated = await resp.json();
      setData((prev) => ({ ...prev, preferences: updated }));
    } catch (e) {
      setError(`Failed to save preferences: ${e.message}`);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div>Loading dashboard...</div>;
  if (error) return <div style={{ color: "red" }}>{error}</div>;

  return (
    <div className="dashboard">
      <h1>Welcome to Your Language Coach Dashboard</h1>

      {/* Progress Section */}
      <section className="progress">
        <h2>Current Progress</h2>
        {data.progress !== null ? (
          <p>
            You have completed <strong>{data.progress.completed}</strong> out of{" "}
            <strong>{data.progress.total}</strong> lessons
            ({data.progress.percentage}%).
          </p>
        ) : (
          <p>No progress data available.</p>
        )}
      </section>

      {/* Upcoming Activities Section */}
      <section className="upcoming">
        <h2>Upcoming Activities</h2>
        {data.upcoming.length > 0 ? (
          <ul>
            {data.upcoming.map((act, idx) => (
              <li key={idx}>
                <strong>{act.title}</strong> – {act.scheduled_date}
              </li>
            ))}
          </ul>
        ) : (
          <p>No upcoming activities.</p>
        )}
      </section>

      {/* Preferences Section */}
      <section className="preferences">
        <h2>Learning Preferences</h2>
        <form onSubmit={handlePrefSubmit}>
          <label>
            Language:
            <input
              type="text"
              name="language"
              value={prefInput.language}
              onChange={handlePrefChange}
              placeholder={data.preferences.language || "e.g., Spanish"}
              required
            />
          </label>
          <br />
          <label>
            Level:
            <select
              name="level"
              value={prefInput.level}
              onChange={handlePrefChange}
              required
            >
              <option value="">Select level</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </label>
          <br />
          <button type="submit" disabled={saving}>
            {saving ? "Saving…" : "Save Preferences"}
          </button>
        </form>
        {data.preferences && (
          <div className="current-prefs">
            <h3>Current Saved Preferences</h3>
            <p>
              Language: <strong>{data.preferences.language}</strong>
            </p>
            <p>
              Level: <strong>{data.preferences.level}</strong>
            </p>
          </div>
        )}
      </section>
    </div>
  );
};

export default Dashboard;