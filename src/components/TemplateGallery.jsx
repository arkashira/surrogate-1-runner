import React from 'react';
import { useTemplates } from '../hooks/useTemplates';

const TemplateGallery = () => {
  const { templates, error, isLoading } = useTemplates();

  if (isLoading) {
    return <div className="loading-state">Loading templates...</div>;
  }

  if (error) {
    return <div className="error-state">Error: {error.message}</div>;
  }

  if (templates.length === 0) {
    return <div className="empty-state">No templates available</div>;
  }

  return (
    <div className="template-gallery">
      <h1>Template Gallery</h1>
      <div className="template-grid">
        {templates.map((template) => (
          <div key={template.id} className="template-card">
            <h2>{template.name}</h2>
            <p className="template-description">{template.description}</p>
            <button
              className="customize-button"
              onClick={() => handleTemplateSelection(template)}
            >
              Customize Template
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

const handleTemplateSelection = (template) => {
  // Implement actual template selection logic here
  console.log('Selected template:', template);
  // Example: navigate to customization page or open modal
};

export default TemplateGallery;