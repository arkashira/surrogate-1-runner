import React, { useState } from 'react';
import { Button } from 'react-bootstrap';
import TemplatePickerModal from './TemplatePickerModal';

const Dashboard: React.FC = () => {
  const [showTemplatePicker, setShowTemplatePicker] = useState(false);

  return (
    <div>
      <h1>Dashboard</h1>
      <Button variant="primary" onClick={() => setShowTemplatePicker(true)}>
        Browse Templates
      </Button>
      <TemplatePickerModal
        show={showTemplatePicker}
        onHide={() => setShowTemplatePicker(false)}
      />
    </div>
  );
};

export default Dashboard;