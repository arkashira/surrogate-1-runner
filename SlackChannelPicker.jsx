// /opt/axentx/surrogate-1/frontend/src/components/SlackChannelPicker.jsx
import React, { useEffect, useState, useCallback } from "react";
import PropTypes from "prop-types";

/**
 * SlackChannelPicker
 *
 * Props
 * -----
 *  - selectedChannelId (string) – currently selected Slack channel ID.
 *  - onChange (func) – called with the new channel ID whenever the user picks one.
 *
 * Behaviour
 * ---------
 * 1. On mount it calls the backend endpoint `/api/slack/channels`.
 *    The backend must use the stored encrypted OAuth token to invoke
 *    Slack’s `conversations.list` API and return JSON shaped like:
 *
 *    {
 *      ok: true,
 *      channels: [{ id: "C12345", name: "general" }, …]
 *    }
 *
 * 2. While the request is in flight a loading message is shown.
 * 3. If the request fails (network error, non‑2xx HTTP, or Slack `ok: false`)
 *    an error UI with a retry button is displayed.
 * 4. When data is available a native `<select>` is rendered.  The parent can
 *    style the component via the supplied CSS class names.
 */
export default function SlackChannelPicker({ selectedChannelId, onChange }) {
  // -------------------------------------------------------------------------
  // State
  // -------------------------------------------------------------------------
  const [channels, setChannels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // -------------------------------------------------------------------------
  // Data fetcher – memoised so it can be used as a stable dependency for useEffect
  // -------------------------------------------------------------------------
  const fetchChannels = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const resp = await fetch("/api/slack/channels", {
        credentials: "include",               // send session cookie / auth token
        headers: { "Accept": "application/json" },
      });

      // ---- HTTP‑level error -------------------------------------------------
      if (!resp.ok) {
        const body = await resp.text();
        throw new Error(`HTTP ${resp.status}: ${body || resp.statusText}`);
      }

      // ---- Payload validation ------------------------------------------------
      const data = await resp.json();

      // Slack may return `{ ok: false, error: "invalid_auth" }`
      if (!data.ok) {
        const msg = data.error ? `Slack error: ${data.error}` : "Slack API error";
        throw new Error(msg);
      }

      // Ensure we have an array; otherwise fall back to empty list (so UI still works)
      const list = Array.isArray(data.channels) ? data.channels : [];
      setChannels(list);
    } catch (e) {
      console.error("[SlackChannelPicker] Failed to load channels:", e);
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []); // no external deps → stable reference

  // -------------------------------------------------------------------------
  // Initial load
  // --------
