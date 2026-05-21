import React, { useState, useEffect } from 'react';
import { Modal, Button } from 'react-bootstrap';

const TerminalModal = ({ show, onHide, onTimeout }) => {
  const [idleTime, setIdleTime] = useState(0);

  useEffect(() => {
    const idleInterval = setInterval(() => {
      setIdleTime(prevTime => prevTime + 1);
    }, 60000);

    return () => clearInterval(idleInterval);
  }, []);

  useEffect(() => {
    if (idleTime >= 24 * 60) {
      onTimeout();
    }
  }, [idleTime, onTimeout]);

  return (
    <Modal show={show} onHide={onHide} size="lg" aria-labelledby="contained-modal-title-vcenter" centered>
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          Session Timeout
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <h4>Your session will be disconnected in {24 * 60 - idleTime} minutes due to inactivity.</h4>
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={onHide}>Extend Session</Button>
      </Modal.Footer>
    </Modal>
  );
};

export default TerminalModal;