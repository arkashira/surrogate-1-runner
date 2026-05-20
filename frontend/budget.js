import React, { useState } from 'react';
import axios from 'axios';

const Budget = () => {
  const [budget, setBudget] = useState(0);
  const [forecast, setForecast] = useState(0);

  const setBudgetHandler = async (e) => {
    e.preventDefault();
    await axios.post('/api/budget', { budget });
    // TODO: Show success message
  };

  const fetchForecast = async () => {
    const response = await axios.get('/api/forecast');
    setForecast(response.data.forecast);
  };

  useEffect(() => {
    fetchForecast();
  }, []);

  return (
    <div>
      <h2>Budget</h2>
      <form onSubmit={setBudgetHandler}>
        <label>
          Set Budget:
          <input type="number" value={budget} onChange={e => setBudget(e.target.value)} />
        </label>
        <button type="submit">Set Budget</button>
      </form>
      <h3>Forecast: ${forecast.toFixed(2)}</h3>
    </div>
  );
};

export default Budget;