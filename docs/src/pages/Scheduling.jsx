import React from 'react';
import Tooltip from '../components/Tooltip';
import { featureDocs } from '../featureDocs';

const Scheduling = () => (
  <div>
    <h1>{featureDocs.scheduling.title}</h1>
    <Tooltip featureId="scheduling" docs={featureDocs} />
    {/* Rest of the page */}
  </div>
);

export default Scheduling;