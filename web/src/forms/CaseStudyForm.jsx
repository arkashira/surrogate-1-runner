import React, { useState } from 'react';
import axios from 'axios';

const CaseStudyForm = () => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    approach: '',
    results: '',
  });
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await axios.post('/api/case-studies', formData);
      setSuccess(true);
      setFormData({ title: '', description: '', approach: '', results: '' });
      setError('');
    } catch (error) {
      console.error('Error submitting case study:', error);
      setError('Failed to submit case study.');
      setSuccess(false);
    }
  };

  return (
    <div>
      <h2>Submit Your Case Study</h2>
      {success && <p>Case study submitted successfully!</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="title">Title:</label>
          <input type="text" id="title" name="title" value={formData.title} onChange={handleChange} required />
        </div>
        <div>
          <label htmlFor="description">Description:</label>
          <textarea id="description" name="description" value={formData.description} onChange={handleChange} required></textarea>
        </div>
        <div>
          <label htmlFor="approach">Approach:</label>
          <textarea id="approach" name="approach" value={formData.approach} onChange={handleChange} required></textarea>
        </div>
        <div>
          <label htmlFor="results">Results:</label>
          <textarea id="results" name="results" value={formData.results} onChange={handleChange} required></textarea>
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default CaseStudyForm;