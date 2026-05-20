import React from 'react';
import FeedbackForm from './FeedbackForm';
import Surrogate1Dashboard from './Surrogate1Dashboard'; // or whatever the main layout is

const FeedbackFormIntegration: React.FC = () => {
  return (
    <Surrogate1Dashboard>
      <FeedbackForm
        onSuccess={(result) => console.log('Feedback stored & analysed', result)}
        onError={(err) => console.error('Feedback error', err)}
      />
    </Surrogate1Dashboard>
  );
};

export default FeedbackFormIntegration;