import React, { useState } from 'react';
import { Modal, Button, Form, Alert } from 'react-bootstrap';

const EmailReportModal = ({ 
  show, 
  onHide, 
  reportData, 
  onSendEmail 
}) => {
  const [emailAddresses, setEmailAddresses] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [sendError, setSendError] = useState('');
  const [sendSuccess, setSendSuccess] = useState(false);

  const validateEmails = (emails) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emails
      .split(',')
      .map(email => email.trim())
      .filter(email => email.length > 0)
      .every(email => emailRegex.test(email));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSendError('');
    setSendSuccess(false);

    if (!validateEmails(emailAddresses)) {
      setSendError('Please enter valid email addresses separated by commas.');
      return;
    }

    setIsSending(true);
    
    try {
      await onSendEmail({
        emails: emailAddresses.split(',').map(email => email.trim()),
        reportData
      });
      setSendSuccess(true);
      setEmailAddresses('');
    } catch (error) {
      setSendError(error.message || 'Failed to send email');
    } finally {
      setIsSending(false);
    }
  };

  const handleClose = () => {
    setSendError('');
    setSendSuccess(false);
    setEmailAddresses('');
    onHide();
  };

  return (
    <Modal show={show} onHide={handleClose} centered>
      <Form onSubmit={handleSubmit}>
        <Modal.Header closeButton>
          <Modal.Title>Send Report via Email</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {sendSuccess && (
            <Alert variant="success">
              Email sent successfully!
            </Alert>
          )}
          {sendError && (
            <Alert variant="danger">
              {sendError}
            </Alert>
          )}
          <Form.Group className="mb-3">
            <Form.Label>Email Addresses</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              value={emailAddresses}
              onChange={(e) => setEmailAddresses(e.target.value)}
              placeholder="Enter one or more email addresses separated by commas"
              required
            />
            <Form.Text className="text-muted">
              Example: user1@example.com, user2@example.com
            </Form.Text>
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose} disabled={isSending}>
            Cancel
          </Button>
          <Button 
            variant="primary" 
            type="submit" 
            disabled={isSending}
          >
            {isSending ? 'Sending...' : 'Send Email'}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default EmailReportModal;