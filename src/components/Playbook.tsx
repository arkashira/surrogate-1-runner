import React, { useState, useEffect } from 'react';
import { generatePlaybook } from '../utils/playbookGenerator';
import { FeedbackForm } from './FeedbackForm';

interface PlaybookProps {
  productMetrics: any;
  niche: string;
}

export const Playbook: React.FC<PlaybookProps> = ({ productMetrics, niche }) => {
  const [playbook, setPlaybook] = useState<any>(null);
  const [feedback, setFeedback] = useState<string>('');

  useEffect(() => {
    const fetchPlaybook = async () => {
      const generatedPlaybook = await generatePlaybook(productMetrics, niche);
      setPlaybook(generatedPlaybook);
    };

    fetchPlaybook();
  }, [productMetrics, niche]);

  const handleFeedbackSubmit = (feedback: string) => {
    setFeedback(feedback);
    // Here you would typically send the feedback to your backend
    console.log('Feedback submitted:', feedback);
  };

  if (!playbook) {
    return <div>Loading playbook...</div>;
  }

  return (
    <div className="playbook-container">
      <h1>Marketing Playbook</h1>
      <div className="playbook-content">
        <h2>Strategies</h2>
        {playbook.strategies.map((strategy: any, index: number) => (
          <div key={index} className="strategy">
            <h3>{strategy.title}</h3>
            <p>{strategy.description}</p>
            <ul>
              {strategy.actions.map((action: string, actionIndex: number) => (
                <li key={actionIndex}>{action}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <FeedbackForm onSubmit={handleFeedbackSubmit} />
    </div>
  );
};