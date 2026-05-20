import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";

/**
 * ProviderList component
 *
 * Renders a list of LLM providers that are registered via a JSON
 * configuration file (e.g. `providers.json`). The component fetches the
 * configuration on mount and displays each provider's name and a short
 * description. If the fetch fails, a fallback message is shown.
 *
 * The JSON file is expected to have the following shape:
 * [
 *   {
 *     "id": "minimax",
 *     "name": "Minimax",
 *     "description": "Minimax LLM provider",
 *     "defaultModel": "mini-1b"
 *   },
 *   ...
 * ]
 *
 * The UI does not make any assumptions about the provider internals – it
 * simply lists what is present in the config, satisfying the acceptance
 * criteria that a newly added provider appears in the UI without code
 * changes.
 */
export default function ProviderList({ configUrl }) {
  const [providers, setProviders] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch the provider configuration on component mount
  useEffect(() => {
    const fetchProviders = async () => {
      try {
        const response = await fetch(configUrl, {
          headers: { "Accept": "application/json" },
        });
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        const data = await response.json();
        // Ensure we have an array; otherwise default to empty list
        setProviders(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error("Failed to load providers:", err);
        setError(err.message || "An unknown error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchProviders();
  }, [configUrl]);

  if (loading) {
    return <div className="provider-list-loading">Loading providers…</div>;
  }

  if (error) {
    return (
      <div className="provider-list-error">
        Unable to load providers. Please check the configuration.
      </div>
    );
  }

  if (providers.length === 0) {
    return (
      <div className="provider-list-empty">
        No LLM providers are currently registered.
      </div>
    );
  }

  return (
    <div className="provider-list">
      <h2>Available LLM Providers</h2>
      <ul className="provider-list-items">
        {providers.map((provider) => (
          <li key={provider.id} className="provider-item">
            <h3 className="provider-name">{provider.name}</h3>
            {provider.description && (
              <p className="provider-description">{provider.description}</p>
            )}
            {provider.defaultModel && (
              <p className="provider-default-model">
                Default model: <strong>{provider.defaultModel}</strong>
              </p>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

ProviderList.propTypes = {
  /** URL to the JSON configuration file that lists providers */
  configUrl: PropTypes.string.isRequired,
};