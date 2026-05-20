
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [presetList, setPresetList] = useState([]);
  const [jobList, setJobList] = useState([]);

  useEffect(() => {
    fetchPresetList();
    fetchJobList();
  }, []);

  async function fetchPresetList() {
    const response = await axios.get('/api/presets');
    setPresetList(response.data);
  }

  async function fetchJobList() {
    const response = await axios.get('/api/jobs');
    setJobList(response.data);
  }

  return (
    <div>
      {/* Preset UI goes here */}
      <h2>Recent Jobs</h2>
      <ul>
        {jobList.map(job => (
          <li key={job.id}>{job.status} - {job.creationTime}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;