import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

/**
 * AccessControls component
 *
 * Displays the current RBAC access level for the logged-in user and
 * allows the user to change it. The component communicates with the
 * Surrogate-1 RBAC API to fetch and update the role.
 *
 * Props:
 *  - apiBase (string): Base URL for the RBAC API (default: '/api/rbac')
 *  - onRoleChange (function): Optional callback invoked after a successful role update
 */
const AccessControls = ({ apiBase = '/api/rbac', onRoleChange }) => {
  const [role, setRole] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [updating, setUpdating] = useState(false);

  const roleOptions = [
    { value: 'admin', label: 'Admin' },
    { value: 'engineer', label: 'Engineer' },
    { value: 'read-only', label: 'Read‑Only' },
  ];

  // Fetch current role on mount
  useEffect(() => {
    const fetchRole = async () => {
      try {
        const res = await fetch(`${apiBase}/role`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setRole(data.role);
      } catch (err) {
        setError(`Failed to load role: ${err.message}`);
      } finally {
        setLoading(false);
      }
    };
    fetchRole();
  }, [apiBase]);

  // Handle role change
  const handleChange = async (e) => {
    const newRole = e.target.value;
    setUpdating(true);
    setError(null);
    try {
      const res = await fetch(`${apiBase}/role`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role: newRole }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setRole(data.role);
      if (onRoleChange) onRoleChange(data.role);
    } catch (err) {
      setError(`Failed to update role: ${err.message}`);
    } finally {
      setUpdating(false);
    }
  };

  if (loading) return <p>Loading access level...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div className="access-controls">
      <label htmlFor="role-select">Access Level:</label>
      <select
        id="role-select"
        value={role}
        onChange={handleChange}
        disabled={updating}
      >
        {roleOptions.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      {updating && <span className="spinner" aria-label="Updating...">⏳</span>}
    </div>
  );
};

AccessControls.propTypes = {
  apiBase: PropTypes.string,
  onRoleChange: PropTypes.func,
};

export default AccessControls;