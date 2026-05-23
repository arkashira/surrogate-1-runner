import React, { useState, useEffect } from 'react';
import { Modal, Button, ListGroup } from 'react-bootstrap';
import { useSurrogateContext } from '../contexts/SurrogateContext';

interface Template {
  name: string;
  description: string;
  content: string;
}

const TemplatePickerModal: React.FC<{ show: boolean; onHide: () => void }> = ({ show, onHide }) => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const { setSurrogateYaml } = useSurrogateContext();

  useEffect(() => {
    const fetchTemplates = async () => {
      const response = await fetch('/api/templates');
      const data = await response.json();
      setTemplates(data);
    };

    fetchTemplates();
  }, []);

  const handleTemplateSelect = (template: Template) => {
    if (window.confirm(`Are you sure you want to apply the ${template.name} template?`)) {
      setSurrogateYaml(template.content);
      onHide();
    }
  };

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Select a Template</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <ListGroup>
          {templates.map((template) => (
            <ListGroup.Item
              key={template.name}
              action
              onClick={() => handleTemplateSelect(template)}
            >
              <h5>{template.name}</h5>
              <p>{template.description}</p>
            </ListGroup.Item>
          ))}
        </ListGroup>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default TemplatePickerModal;