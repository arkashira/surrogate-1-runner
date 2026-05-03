import React from 'react';
import { useLibraryStore } from '../lib/libraryStore';
import { openDocumentInViewer } from '../lib/viewer';

export function LibraryList() {
- const { documents, selectedId, selectDocument } = useLibraryStore();
+ const { getOrderedDocuments, selectedId, openDocument } = useLibraryStore();
+ const documents = getOrderedDocuments();

  const handleClick = async (id: string) => {
+   // Mark as opened (pins to top + tracks)
+   openDocument(id);
+
    // Open in viewer (embedded or system default) within 1s
    await openDocumentInViewer(id);
  };

  return (
    <div className="library-list">
      {documents.map((doc) => (
        <div
          key={doc.id}
          className={`library-item ${selectedId === doc.id ? 'selected' : ''}`}
          onClick={() => handleClick(doc.id)}
          role="button"
          tabIndex={0}
        >
          <span className="doc-name">{doc.name}</span>
          <span className="doc-meta">{formatSize(doc.size)}</span>
        </div>
      ))}
    </div>
  );
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}