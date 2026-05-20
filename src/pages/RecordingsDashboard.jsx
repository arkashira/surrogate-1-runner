import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';

const RecordingsDashboard = () => {
  const [recordings, setRecordings] = useState([]);

  useEffect(() => {
    fetchRecordings();
  }, []);

  const fetchRecordings = async () => {
    try {
      const response = await axios.get('/api/recordings');
      setRecordings(response.data);
    } catch (error) {
      console.error('Error fetching recordings:', error);
    }
  };

  return (
    <div className="recordings-dashboard">
      <h1>Recorded Sessions</h1>
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Date</th>
            <th>Duration</th>
          </tr>
        </thead>
        <tbody>
          {recordings.map((recording, index) => (
            <tr key={index}>
              <td>{recording.title}</td>
              <td>{recording.date}</td>
              <td>{recording.duration} mins</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RecordingsDashboard;