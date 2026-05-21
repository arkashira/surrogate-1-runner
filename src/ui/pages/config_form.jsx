import React, { useState } from 'react';

const ConfigForm = () => {
  const [dataType, setDataType] = useState('metrics');
  const [dataVolume, setDataVolume] = useState(1000);
  const [startTimestamp, setStartTimestamp] = useState('');
  const [endTimestamp, setEndTimestamp] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Implement saving user configurations
    console.log('Form submitted:', { dataType, dataVolume, startTimestamp, endTimestamp });
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Data Type:
        <select value={dataType} onChange={e => setDataType(e.target.value)}>
          <option value="metrics">Metrics</option>
          <option value="logs">Logs</option>
          <option value="traces">Traces</option>
        </select>
      </label>
      <br />
      <label>
        Data Volume:
        <input type="number" value={dataVolume} onChange={e => setDataVolume(e.target.value)} />
      </label>
      <br />
      <label>
        Start Timestamp:
        <input type="datetime-local" value={startTimestamp} onChange={e => setStartTimestamp(e.target.value)} />
      </label>
      <br />
      <label>
        End Timestamp:
        <input type="datetime-local" value={endTimestamp} onChange={e => setEndTimestamp(e.target.value)} />
      </label>
      <br />
      <button type="submit">Save</button>
    </form>
  );
};

export default ConfigForm;