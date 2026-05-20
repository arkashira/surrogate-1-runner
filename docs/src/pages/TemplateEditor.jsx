import React from 'react';
import Tooltip from '../components/Tooltip';
import { featureDocs } from '../featureDocs';

const TemplateEditor = () => (
  <div>
    <h1>{featureDocs.templateEditor.title}</h1>
    <Tooltip featureId="templateEditor" docs={featureDocs} />
    {/* Rest of the page */}
  </div>
);

export default TemplateEditor;