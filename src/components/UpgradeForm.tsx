import React, { useState } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { UpgradeRecommendation } from '../types/UpgradeRecommendation';

interface FormData {
  cpu: string;
  gpu: string;
  ram: string;
  budget: number;
}

const schema = yup.object().shape({
  cpu: yup.string().required('CPU is required'),
  gpu: yup.string().required('GPU is required'),
  ram: yup.string().required('RAM is required'),
  budget: yup.number().required('Budget is required').positive('Budget must be positive'),
});

const UpgradeForm: React.FC = () => {
  const [recommendations, setRecommendations] = useState<UpgradeRecommendation[]>([]);
  const [error, setError] = useState<string>('');
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: yupResolver(schema),
  });

  const onSubmit: SubmitHandler<FormData> = async (data) => {
    try {
      const response = await fetch('/api/upgrade-recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }

      const result = await response.json();
      setRecommendations(result.recommendations);
      setError('');
    } catch (err) {
      setError(err.message);
      setRecommendations([]);
    }
  };

  const handleSelect = (recommendation: UpgradeRecommendation) => {
    // Logic to handle the selection of a recommendation
    console.log('Selected recommendation:', recommendation);
  };

  return (
    <div className="upgrade-form">
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="form-group">
          <label htmlFor="cpu">CPU</label>
          <input id="cpu" {...register('cpu')} />
          {errors.cpu && <p className="error">{errors.cpu.message}</p>}
        </div>
        <div className="form-group">
          <label htmlFor="gpu">GPU</label>
          <input id="gpu" {...register('gpu')} />
          {errors.gpu && <p className="error">{errors.gpu.message}</p>}
        </div>
        <div className="form-group">
          <label htmlFor="ram">RAM</label>
          <input id="ram" {...register('ram')} />
          {errors.ram && <p className="error">{errors.ram.message}</p>}
        </div>
        <div className="form-group">
          <label htmlFor="budget">Budget (USD)</label>
          <input id="budget" type="number" {...register('budget')} />
          {errors.budget && <p className="error">{errors.budget.message}</p>}
        </div>
        <button type="submit">Get Recommendations</button>
      </form>
      {error && <p className="error">{error}</p>}
      {recommendations.length > 0 && (
        <div className="recommendations">
          <h2>Top 3 Upgrade Recommendations</h2>
          <ul>
            {recommendations.map((rec, index) => (
              <li key={index}>
                <h3>{rec.componentNames.join(', ')}</h3>
                <p>Price: ${rec.price}</p>
                <p>Expected FPS: {rec.expectedFPS}</p>
                <p>ROI: {rec.roi}</p>
                <button onClick={() => handleSelect(rec)}>Select</button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default UpgradeForm;