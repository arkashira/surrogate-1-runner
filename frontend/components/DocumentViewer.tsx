
import React from 'react';

interface DocumentViewerProps {
  documentUrl: string;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({ documentUrl }) => {
  return (
    <div className="document-viewer">
      <iframe src={documentUrl} width="100%" height="600px" title="Document Viewer" />
    </div>
  );
};

export default DocumentViewer;