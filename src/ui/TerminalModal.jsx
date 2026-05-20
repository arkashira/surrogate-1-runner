import React, { useState } from 'react';
import { Modal, Button } from 'antd';
import XTerm from 'xterm';
import 'xterm/css/xterm.css';
import './TerminalModal.css';

const TerminalModal = ({ visible, onClose, nodeId }) => {
  const [terminal, setTerminal] = useState(null);
  const [error, setError] = useState(null);
  const [isConnecting, setIsConnecting] = useState(false);

  const connectToTerminal = async () => {
    setIsConnecting(true);
    setError(null);
    try {
      const ws = new WebSocket(`wss://backend.example.com/terminal/${nodeId}`, ['binary', 'base64']);
      const term = new XTerm();
      term.open(document.getElementById('terminal-container'));
      term.attach(ws);
      setTerminal(term);
      term.write('Connected to terminal.\r\n');
    } catch (err) {
      setError('Failed to connect to terminal. Please check the server address and try again.');
      setIsConnecting(false);
    }
  };

  const handleErrorRetry = () => {
    setError(null);
    connectToTerminal();
  };

  const handleOk = () => {
    if (isConnecting) return; // Prevent duplicate connections
    connectToTerminal();
  };

  return (
    <Modal
      title="Launch Terminal"
      visible={visible}
      onOk={handleOk}
      onCancel={onClose}
      okText="Connect"
      cancelText="Cancel"
      width="100%"
      footer={[
        <Button key="retry" onClick={handleErrorRetry} disabled={!error}>
          Retry
        </Button>,
        <Button key="cancel" onClick={onClose}>
          Cancel
        </Button>,
      ]}
    >
      {error ? (
        <div className="error-message">
          <p>{error}</p>
          <Button onClick={handleErrorRetry}>Retry</Button>
        </div>
      ) : isConnecting ? (
        <div className="connecting-message">Connecting to server...</div>
      ) : (
        <div id="terminal-container" className="terminal-container"></div>
      )}
    </Modal>
  );
};

export default TerminalModal;