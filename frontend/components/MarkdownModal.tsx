import React, { useState } from 'react';
import Modal from 'react-modal';
import marked from 'marked';

interface MarkdownModalProps {
  isOpen: boolean;
  onRequestClose: () => void;
  markdownContent: string;
}

const MarkdownModal: React.FC<MarkdownModalProps> = ({ isOpen, onRequestClose, markdownContent }) => {
  const [htmlContent, setHtmlContent] = useState('');

  React.useEffect(() => {
    if (markdownContent) {
      setHtmlContent(marked(markdownContent));
    }
  }, [markdownContent]);

  return (
    <Modal isOpen={isOpen} onRequestClose={onRequestClose}>
      <div className="modal-content">
        <button onClick={onRequestClose}>Close</button>
        <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
      </div>
    </Modal>
  );
};

export default MarkdownModal;