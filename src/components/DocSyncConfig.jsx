import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';

/**
 * DocSyncConfig Component
 * 
 * Features:
 * - Fetches repo list from API.
 * - Checks user roles to determine if toggle is editable.
 * - Uses Optimistic UI updates (updates state before server response).
 * - Reverts state automatically if the API call fails.
 */
const DocSyncConfig = ({ userRoleMap = {} }) => {
  const [repositories, setRepositories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRepositories();
  }, []);

  const fetchRepositories = async () => {
    try {
      // Using endpoint from Candidate 1 (specific to doc-sync)
      const response = await axios.get('/api/v1/doc-sync/repositories');
      setRepositories(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch repositories');
      setLoading(false);
    }
  };

  const handleToggle = async (repoId, currentEnabled) => {
    const newEnabledState = !currentEnabled;
    const repo = repositories.find(r => r.id === repoId);
    
    // 1. OPTIMISTIC UPDATE: Update UI immediately
    setRepositories(prev => prev.map(repo => 
      repo.id === repoId ? { ...repo, enabled: newEnabledState } : repo
    ));

    try {
      // 2. API CALL: Using payload structure from Candidate 2 (includes defaultBranch)
      await axios.patch('/api/v1/doc-sync/config', {
        repoId,
        enabled: newEnabledState,
        // Only send branch if enabling, or grab current branch
        defaultBranch: newEnabledState ? repo.defaultBranch : null,
      });
    } catch (err) {
      console.error('Failed to update DocSync config:', err);
      
      // 3. REVERT: If failed, revert UI to previous state (Correctness)
      setRepositories(prev => prev.map(repo => 
        repo.id === repoId ? { ...repo, enabled: currentEnabled } : repo
      ));
      
      // Optional: Show a toast notification here in a real app
      setError('Failed to update settings. Changes reverted.');
      setTimeout(() => setError(null), 3000);
    }
  };

  if (loading) return <div className="p-4 text-gray-500">Loading repositories...</div>;
  if (error) return <div className="p-4 text-red-500 bg-red-50 rounded">{error}</div>;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">DocSync Configuration</h1>
      
      <div className="space-y-4">
        {repositories.map((repo) => {
          // RBAC Check: Only 'admin' can edit
          const userRole = userRoleMap[repo.id];
          const canEdit = userRole === 'admin';

          return (
            <div key={repo.id} className="bg-white border border-gray-200 rounded-lg p-4 flex items-center justify-between shadow-sm hover:shadow-md transition-shadow">
              <div>
                <h2 className="font-semibold text-lg">{repo.name}</h2>
                <p className="text-sm text-gray-500">Default branch: {repo.defaultBranch}</p>
                {repo.latestPreview && (
                  <a 
                    href={repo.latestPreview.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline text-sm mt-2 inline-flex items-center"
                  >
                    View latest preview &rarr;
                  </a>
                )}
              </div>

              {/* Toggle Switch UI (Tailwind) */}
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={repo.enabled || false}
                  disabled={!canEdit} // Disable input if not admin
                  onChange={() => handleToggle(repo.id, repo.enabled)}
                  className="sr-only peer"
                />
                <div className={`
                  w-11 h-6 bg-gray-200 rounded-full peer peer-checked:after:translate-x-full 
                  peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 
                  after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full 
                  after:h-5 after:w-5 after:transition-all
                  ${canEdit ? 'peer-checked:bg-blue-600 cursor-pointer' : 'peer-checked:bg-gray-400 cursor-not-allowed opacity-75'}
                `}></div>
                <span className="ml-3 text-sm font-medium text-gray-700">
                  {canEdit ? (repo.enabled ? 'Enabled' : 'Disabled') : (repo.enabled ? 'Enabled' : 'Disabled')}
                </span>
              </label>
            </div>
          );
        })}
      </div>
    </div>
  );
};

DocSyncConfig.propTypes = {
  userRoleMap: PropTypes.object,
};

export default DocSyncConfig;