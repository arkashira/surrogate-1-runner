
import React, { useState } from 'react';
import { Button, Form } from 'react-bootstrap';

const Confirm = () => {
  const [apiKey, setApiKey] = useState('');
  const [provider, setProvider] = useState('OpenAI');
  const [model, setModel] = useState('GPT-3.5');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Validate API key and proceed to start using Surrogate-1
  };

  return (
    <Form onSubmit={handleSubmit}>
      <h2>Confirm Settings</h2>
      <Form.Group controlId="apiKey">
        <Form.Label>API Key</Form.Label>
        <Form.Control type="text" value={apiKey} onChange={(e) => setApiKey(e.target.value)} />
      </Form.Group>
      <Form.Group controlId="provider">
        <Form.Label>LLM Provider</Form.Label>
        <Form.Control as="select" value={provider} onChange={(e) => setProvider(e.target.value)}>
          <option value="OpenAI">OpenAI</option>
          <option value="Anthropic">Anthropic</option>
          <option value="Cohere">Cohere</option>
        </Form.Control>
      </Form.Group>
      <Form.Group controlId="model">
        <Form.Label>Model</Form.Label>
        <Form.Control as="select" value={model} onChange={(e) => setModel(e.target.value)}>
          <option value="GPT-3.5">GPT-3.5</option>
          {/* Add more model options here */}
        </Form.Control>
      </Form.Group>
      <Button variant="primary" type="submit">
        Start Using
      </Button>
    </Form>
  );
};

export default Confirm;