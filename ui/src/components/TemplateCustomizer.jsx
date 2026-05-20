import React, { useState, useEffect } from 'react';
import './TemplateCustomizer.css';

const TemplateCustomizer = () => {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [config, setConfig] = useState({});

  useEffect(() => {
    fetch('/templates.json')
      .then((res) => res.json())
      .then((data) => setTemplates(data));
  }, []);

  const handleSelect = (template) => {
    setSelectedTemplate(template);
    setConfig(template.config);
  };

  const handleChange = (key, value) => {
    setConfig((prev) => ({ ...prev, [key]: value }));
  };

  const handleSave = () => {
    if (!selectedTemplate) return;
    // In a real app this would POST to an API
    console.log('Saved config for', selectedTemplate.id, config);
    alert('Configuration saved!');
  };

  const categories = Array.from(new Set(templates.map((t) => t.category)));

  return (
    // ... (same as Candidate 1)
  );
};

export default TemplateCustomizer;