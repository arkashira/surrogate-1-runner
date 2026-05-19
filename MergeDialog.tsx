import React, { useState } from 'react';
import { InventoryItem } from '../types';

interface Props {
  local: InventoryItem;
  remote: InventoryItem;
  onResolve: (resolved: InventoryItem) => void;
  onCancel: () => void;
}

export const MergeDialog: React.FC<Props> = ({ local, remote, onResolve, onCancel }) => {
  const [choice, setChoice] = useState<'local' | 'remote'>('local');
  const [merged, setMerged] = useState<InventoryItem>(local);

  const handleUseLocal = () => {
    setChoice('local');
    setMerged(local);
  };

  const handleUseRemote = () => {
    setChoice('remote');
    setMerged(remote);
  };

  const handleMerge = () => {
    // Simple merge: keep fields from both sides.  
    // Replace with your own business logic if needed.
    const mergedItem: InventoryItem = {
      ...remote,
      ...local,
      updatedAt: Date.now(),
    };
    onResolve(mergedItem);
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-2xl w-full">
        <h3 className="text-lg font-semibold mb-4">Conflict Detected</h3>
        <p className="text-sm text-gray-600 mb-4">
          Another user modified this item while you were editing. Choose which version to keep or merge manually.
        </p>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="border rounded p-3">
            <h4 className="font-medium mb-2">Your Version (Local)</h4>
            <pre className="text-xs bg-gray-50 p-2 rounded">{JSON.stringify(local, null, 2)}</pre>
            <button
              onClick={handleUseLocal}
              className={`mt-2 w-full py-1 px-3 rounded ${choice === 'local' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            >
              Use Local
            </button>
          </div>

          <div className="border rounded p-3">
            <h4 className="font-medium mb-2">Remote Version</h4>
            <pre className="text-xs bg-gray-50 p-2 rounded">{JSON.stringify(remote, null, 2)}</pre>
            <button
              onClick={handleUseRemote}
              className={`mt-2 w-full py-1 px-3 rounded ${choice === 'remote' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            >
              Use Remote
            </button>
          </div>
        </div>

        <div className="flex justify-end gap-2">
          <button onClick={onCancel} className="px-4 py-2 text-gray-600">
            Cancel
          </button>
          <button onClick={handleMerge} className="px-4 py-2 bg-blue-600 text-white rounded">
            Merge & Resolve
          </button>
        </div>
      </div>
    </div>
  );
};