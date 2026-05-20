import React, { useState, useEffect, useCallback } from 'react';
import { useAppDispatch, useAppSelector } from '../redux/store';
import { setThreshold, setNotificationMethod } from '../redux/alertSlice';

const AlertConfiguration: React.FC = () => {
  const dispatch = useAppDispatch();
  const { threshold, notificationMethod } = useAppSelector((s) => s.alert);

  // Local form state
  const [localThreshold, setLocalThreshold] = useState(threshold);
  const [localMethod, setLocalMethod] = useState(notificationMethod);
  const [touched, setTouched] = useState(false);

  // Keep local state in sync with store
  useEffect(() => {
    setLocalThreshold(threshold);
    setLocalMethod(notificationMethod);
  }, [threshold, notificationMethod]);

  const isValid = localThreshold >= 5 && localThreshold <= 95;
  const isDirty = localThreshold !== threshold || localMethod !== notificationMethod;

  const handleThresholdChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const val = parseInt(e.target.value, 10);
      if (!isNaN(val)) setLocalThreshold(val);
      setTouched(true);
    },
    []
  );

  const handleMethodChange = useCallback(
    (e: React.ChangeEvent<HTMLSelectElement>) => {
      setLocalMethod(e.target.value as 'email' | 'in-app');
      setTouched(true);
    },
    []
  );

  const handleSave = useCallback(() => {
    if (!isValid) return;
    dispatch(setThreshold(localThreshold));
    dispatch(setNotificationMethod(localMethod));
    setTouched(false);
  }, [dispatch, localThreshold, localMethod, isValid]);

  return (
    <section className="alert-configuration">
      <h2>Alert Configuration</h2>
      <div className="form-group">
        <label htmlFor="threshold">Threshold (%):</label>
        <input
          id="threshold"
          type="number"
          min={5}
          max={95}
          value={localThreshold}
          onChange={handleThresholdChange}
        />
        {!isValid && <small className="error">Must be 5‑95</small>}
      </div>

      <div className="form-group">
        <label htmlFor="method">Notification Method:</label>
        <select id="method" value={localMethod} onChange={handleMethodChange}>
          <option value="email">Email</option>
          <option value="in-app">In‑App</option>
        </select>
      </div>

      <button
        onClick={handleSave}
        disabled={!touched || !isValid || !isDirty}
      >
        Save
      </button>
    </section>
  );
};

export default AlertConfiguration;