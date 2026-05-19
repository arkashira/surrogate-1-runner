import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchUpgradeRecommendations } from '../redux/actions/upgradeActions';
import { RootState } from '../redux/store';

interface UpgradeRecommendation {
  id: string;
  name: string;
  cost: number;
  fpsImprovement: number;
  components: string[];
}

const UpgradeRecommendations: React.FC = () => {
  const [budget, setBudget] = useState<number>(0);
  const [targetGame, setTargetGame] = useState<string>('');
  const dispatch = useDispatch();
  const recommendations = useSelector((state: RootState) => state.upgrade.recommendations);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    dispatch(fetchUpgradeRecommendations(budget, targetGame));
  };

  return (
    <div className="upgrade-recommendations">
      <h2>Upgrade Recommendations</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="budget">Budget:</label>
          <input
            type="number"
            id="budget"
            value={budget}
            onChange={(e) => setBudget(parseInt(e.target.value))}
            required
          />
        </div>
        <div>
          <label htmlFor="targetGame">Target Game:</label>
          <input
            type="text"
            id="targetGame"
            value={targetGame}
            onChange={(e) => setTargetGame(e.target.value)}
            required
          />
        </div>
        <button type="submit">Get Recommendations</button>
      </form>
      <div className="recommendations-list">
        {recommendations.map((recommendation: UpgradeRecommendation) => (
          <div key={recommendation.id} className="recommendation">
            <h3>{recommendation.name}</h3>
            <p>Cost: ${recommendation.cost}</p>
            <p>FPS Improvement: {recommendation.fpsImprovement}</p>
            <ul>
              {recommendation.components.map((component, index) => (
                <li key={index}>{component}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default UpgradeRecommendations;