import React, { useState } from 'react';

const Quiz = ({ questions, onSubmit }) => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answer, setAnswer] = useState('');

  const handleAnswerChange = (event) => {
    setAnswer(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(answer, questions[currentQuestion]);
    setCurrentQuestion(currentQuestion + 1);
    setAnswer('');
  };

  if (currentQuestion >= questions.length) {
    return <div>Quiz completed!</div>;
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>{questions[currentQuestion].question}</h2>
      <input type="text" value={answer} onChange={handleAnswerChange} />
      <button type="submit">Submit</button>
    </form>
  );
};

export default Quiz;