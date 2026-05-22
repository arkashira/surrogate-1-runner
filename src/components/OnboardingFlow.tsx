import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { setLearningGoal, setOnboardingFeedback } from '../services/userService';

const OnboardingFlow: React.FC = () => {
  const [step, setStep] = useState(1);
  const [learningGoal, setLearningGoalInput] = useState('');
  const [feedback, setFeedback] = useState('');
  const navigate = useNavigate();

  const handleNextStep = () => {
    if (step === 1 && learningGoal) {
      setLearningGoal(learningGoal);
      setStep(2);
    } else if (step === 2 && feedback) {
      setOnboardingFeedback(feedback);
      navigate('/dashboard');
    }
  };

  return (
    <div className="onboarding-flow">
      {step === 1 && (
        <div className="step">
          <h2>Set Your Learning Goal</h2>
          <input
            type="text"
            value={learningGoal}
            onChange={(e) => setLearningGoalInput(e.target.value)}
            placeholder="What do you want to learn?"
          />
          <button onClick={handleNextStep}>Next</button>
        </div>
      )}
      {step === 2 && (
        <div className="step">
          <h2>Feedback</h2>
          <textarea
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            placeholder="How was your onboarding experience?"
          />
          <button onClick={handleNextStep}>Complete</button>
        </div>
      )}
    </div>
  );
};

export default OnboardingFlow;