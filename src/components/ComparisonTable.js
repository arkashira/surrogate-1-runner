
import React from 'react';
import { Table, Thead, Tbody, Tr, Th, Td } from '@chakra-ui/react';

const freePlan = {
  name: 'Free',
  features: [
    { name: 'Daily data ingest', limit: 1000 },
    { name: 'Concurrent data streams', limit: 1 },
    { name: 'Model training', limit: 'None' },
    { name: 'Model serving', limit: 'None' },
  ],
};

const paidPlan = {
  name: 'Pro',
  features: [
    { name: 'Daily data ingest', limit: 10000 },
    { name: 'Concurrent data streams', limit: 5 },
    { name: 'Model training', limit: 'Unlimited' },
    { name: 'Model serving', limit: 'Unlimited' },
  ],
};

const ComparisonTable = () => {
  return (
    <Table variant="striped" size="sm">
      <Thead>
        <Tr>
          <Th>Feature</Th>
          <Th>Free Tier</Th>
          <Th>Paid Tier</Th>
        </Tr>
      </Thead>
      <Tbody>
        {freePlan.features.map((feature, index) => (
          <Tr key={index}>
            <Td>{feature.name}</Td>
            <Td>{feature.limit}</Td>
            <Td>{paidPlan.features[index].limit}</Td>
          </Tr>
        ))}
      </Tbody>
    </Table>
  );
};

export default ComparisonTable;

// src/components/PlanDetails.js

import React from 'react';
import ComparisonTable from './ComparisonTable';

const PlanDetails = ({ plan }) => {
  return (
    <div>
      <h2>{plan.name}</h2>
      <ComparisonTable />
      {/* Add more plan details if needed */}
    </div>
  );
};

export default PlanDetails;